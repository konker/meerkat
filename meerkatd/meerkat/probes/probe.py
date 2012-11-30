# -*- coding: utf-8 -*-
#
# meerkat.probes.probe
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import traceback
import fcntl
import logging
from subprocess import Popen, PIPE
import pyev
import json


# constants
TYPE_DURATION = 1
TYPE_PERIODIC = 2
TYPE_CONTINUOUS = 4

DATA_TYPE_JSON = 8
DATA_TYPE_TEXT = 16
DATA_TYPE_DATA = 32


class Probe(object):
    def __init__(self, id, index, storage, cache, probe_conf, timeout=-1):
        self.id = id
        self.index = index
        self.storage = storage
        self.cache = cache
        self.command = probe_conf["command"]
        self.data_type = probe_conf["data_type"]
        self.filters = probe_conf["filters"]
        self.error_filters = probe_conf["error_filters"]
        self.interval = probe_conf["interval"]
        self.duration = probe_conf["duration"]
        self.no_store = probe_conf["no_store"]
        self.cache_last = probe_conf["cache_last"]
        self.dummy = probe_conf["dummy"]
        self.timeout = timeout
        self.active = False
        self.running = False
        self.last_error = None
        self.loop = None
        self.process = None
        self.pid = None
        self.buf = None
        self.err_buf = None

        self.watchers = {
            "interval": None,
            "io": {
                "stdout": None,
                "stderr": None
            },
            "duration": None,
            "timeout": None
        }


    def register(self, loop):
        self.loop = loop
        self.init_non_io()
        logging.info("Registered probe: %s" % (self.id))


    def start(self):
        logging.info("[%s] Start" % (self.id))
        if self.running:
            logging.warning("[%s] Start when already running. Skipping" % (self.id))
            return

        self.restart()
        self.running = True


    def restart(self):
        self.active = False
        self.set_interval()


    def stop(self):
        logging.info("[%s] Stop" % (self.id))
        self.running = False
        self.kill_command()
        self.stop_watchers()


    def stop_watchers(self, watchers=None):
        if watchers == None:
            watchers = self.watchers

        for k,w in watchers.items():
            if w:
                if type(w) == type({}):
                    # recurse
                    self.stop_watchers(w)
                else:
                    w.stop()

        self.active = False
        self.running = False


    # execute the command
    def interval_cb(self, watcher, revents):
        logging.debug("[%s] Interval complete: %s secs." % (self.id, self.interval))

        if not self.running:
            logging.warning("[%s] Interval callback when not running. Skipping" % (self.id))
            return

        if self.active:
            logging.warning("[%s] Interval callback when still in active state. Skipping" % (self.id))
            return

        self.active = True
        self.cancel_interval()

        # create a sub-process for the probe command, listen to stdout and stderr
        # NOTE: shell must be False, otherwise duration_cb cannot terminate it properly
        # (cannot terminate child processes of the shell process, e.g. #!/bin/python)
        try:
            self.process = Popen(self.command, bufsize=0, shell=False, stdout=PIPE, stderr=PIPE)
            self.pid = self.process.pid
        except:
            self.handle_error(traceback.format_exc())
            return

        self.buf = []
        self.err_buf = []

        # initialize I/O watchers
        self.set_io()

        # set up a watcher to kill the process after the duration
        if self.duration > 0:
            self.set_duration()

        # set up a watcher to kill the process after a global timeout
        if self.timeout > 0:
            self.set_timeout()


    # read any data available from stdout pipe
    def io_stdout_cb(self, watcher, revents):
        logging.debug("[%s] Stdout ready" % (self.id))
        self.make_nonoblocking(self.process.stdout)

        data = self.process.stdout.read()

        # process the data and re-start the interval
        # when all data has been read
        if data == '': # EOF
            # cancel outstanding watchers
            self.cancel_all()

            data = self.process_data(self.buf)
            if self.is_data(data):
                self.handle_data(data)

            self.restart()
        else:
            self.buf.append(data)


    # read any data available from stderr pipe
    def io_stderr_cb(self, watcher, revents):
        logging.debug("[%s] Stderr ready" % (self.id))
        self.make_nonoblocking(self.process.stderr)

        # read in error data
        error = self.process.stderr.read()

        if error == '': # EOF
            # cancel outstanding watchers
            self.cancel_all()

            error = self.process_error(self.err_buf)
            if self.is_error(error):
                self.handle_error(error)

            self.restart()
        else:
            # XXX: error filters are different from data filters. Data filters are only
            #      applied when all data has been read, before storage. Error filters
            #      are applied as soon as any stderr comes in, and when all errors have
            #      been read. Annoying inconsistency.
            # NOTE: Apply error filters as errors come in, rather than just at the end
            error = self.process_error(error)
            if self.is_error(error):
                # NOTE: any error overrides data that may have been read
                self.cancel_stdout()
                self.err_buf.append(error)


    def duration_cb(self, watcher, revents):
        logging.debug("[%s] Duration complete: %s secs." % (self.id, self.duration))

        # cancel outstanding watchers
        self.cancel_all()

        # terminate the command process
        self.terminate_command()

        # check for error
        # NOTE: any error overrides data that may have been read
        error = self.process_error(self.err_buf)
        if self.is_error(error):
            self.handle_error(error)
        else:
            # OK - deal with the collected data
            data = self.process_data(self.buf)
            if self.is_data(data):
                self.handle_data(data)

        self.restart()


    def timeout_cb(self, watcher, revents):
        logging.debug("[%s] Timeout complete %s secs." % (self.id, self.timeout))

        # cancel outstanding watchers
        self.cancel_all()

        # kill the command process
        self.kill_command()

        # check for error
        # NOTE: any error overrides data that may have been read
        error = self.process_error(self.err_buf)
        if self.is_error(error):
            self.handle_error(error)
        else:
            # OK - deal with the collected data
            self.process_data(self.buf)
            if self.is_data(data):
                self.handle_data(data)

        self.restart()


    def process_error(self, error):
        # deal with a buffer
        if type(error) == list:
            error = ''.join(error)

        # apply error filters
        for filter in self.error_filters:
            error = filter.filter(error)

        return error


    def handle_error(self, error):
        self.last_error = error
        logging.error("Error in probe: %s: %s" % (self.id, self.last_error))


    def is_error(self, error):
        return (error != '' and error != None)


    def process_data(self, data):
        # deal with a buffer
        # basically want to end up with an array (JSON data type)
        if type(data) == list:
            if self.data_type == DATA_TYPE_JSON:
                # XXX: a bit messy
                if len(data) == 1 and data[0].startswith('['):
                    data = data[0]
                elif data[0].startswith('['):
                    data = ''.join(data)
                else:
                    data = '[' + ','.join(data) + ']'
            elif self.data_type == DATA_TYPE_TEXT:
                # [FIXME: do we need this?]
                data = ''.join(data)
            else:
                data = b''.join(data)

        # apply filters
        try:
            for filter in self.filters:
                data = filter.filter(data)
        except:
            self.handle_error(traceback.format_exc())
            return None

        return data


    def handle_data(self, data):
        self.last_error = None

        # store
        if self.storage:
            if not self.no_store:
                logging.debug("[%s] -> %s" % (self.id, data))
                self.storage.write_str(self.id, data)
            else:
                logging.debug("[%s] ->| %s" % (self.id, data))

        # cache
        if self.cache_last:
            if self.data_type == DATA_TYPE_JSON:
                self.cache.put(self.id, json.loads(data))
            else:
                self.cache.put(self.id, data)


    def is_data(self, data):
        return (data != '' and data != None)


    # Set the given pipe to be in non-blocking mode
    def make_nonoblocking(self, pipe):
        fd = pipe.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


    # Terminate the command SIGTERM
    def terminate_command(self):
        logging.debug("[%s] terminate command: SIGTERM %s" % (self.id, self.pid))

        try:
            if self.process:
                self.process.terminate()
        except OSError as ex:
            logging.error("Could not terminate command: %s: %s" % (self.id, self.pid))


    # Kill the command SIGKILL
    def kill_command(self):
        logging.debug("[%s] kill command: SIGKILL %s" % (self.id, self.pid))

        try:
            if self.process:
                self.process.kill()
        except OSError as ex:
            logging.error("Could not kill command: %s: %s" % (self.id, self.pid))


    def cancel_all(self):
        self.cancel_timeout()
        self.cancel_duration()
        self.cancel_io()
        self.cancel_interval()


    def init_all(self):
        self.init_interval()
        self.init_io_stdout()
        self.init_io_stderr()
        self.init_duration()
        self.init_timeout()


    def init_non_io(self):
        self.init_interval()
        self.init_duration()
        self.init_timeout()


    def init_interval(self):
        self.watchers["interval"] = pyev.Timer(self.interval, 0.0, self.loop, self.interval_cb)


    def set_interval(self):
        logging.debug("[%s] Adding interval timer: %s secs." % (self.id, self.interval))

        if not self.watchers["interval"]:
            self.init_interval()
        else:
            self.watchers["interval"].set(self.interval, 0.0)

        self.watchers["interval"].start()


    def cancel_interval(self):
        if self.watchers["interval"] and self.watchers["interval"].active:
            logging.debug("[%s] Cancel interval" % (self.id))
            self.watchers["interval"].stop()


    def init_io_stdout(self):
        self.watchers["io"]["stdout"] = pyev.Io(self.process.stdout, pyev.EV_READ, self.loop, self.io_stdout_cb)


    def init_io_stderr(self):
        self.watchers["io"]["stderr"] = pyev.Io(self.process.stderr, pyev.EV_READ, self.loop, self.io_stderr_cb)


    def set_io(self):
        logging.debug("[%s] Adding I/O watchers" % (self.id))

        # set up watchers for stdout
        if not self.watchers["io"]["stdout"]:
            self.init_io_stdout()
        else:
            self.watchers["io"]["stdout"].set(self.process.stdout, pyev.EV_READ)

        self.watchers["io"]["stdout"].start()

        # set up watchers for stderr
        if not self.watchers["io"]["stderr"]:
            self.init_io_stderr()
        else:
            self.watchers["io"]["stderr"].set(self.process.stderr, pyev.EV_READ)

        self.watchers["io"]["stderr"].start()


    def cancel_io(self):
        self.cancel_stdout()
        self.cancel_stderr()


    def cancel_stdout(self):
        if self.watchers["io"]["stdout"]:
            logging.debug("[%s] Cancel stdout I/O watcher" % (self.id))
            self.watchers["io"]["stdout"].stop()


    def cancel_stderr(self):
        if self.watchers["io"]["stderr"]:
            logging.debug("[%s] Cancel stderr I/O watcher" % (self.id))
            self.watchers["io"]["stderr"].stop()


    def init_duration(self):
        if self.duration > 0:
            self.watchers["duration"] = pyev.Timer(self.duration, 0.0, self.loop, self.duration_cb)


    def set_duration(self):
        logging.debug("[%s] Adding duration timeout: %s secs." % (self.id, self.duration))

        if not self.watchers["duration"]:
            self.init_duration()
        else:
            self.watchers["duration"].set(self.duration, 0.0)

        self.watchers["duration"].start()


    def cancel_duration(self):
        if self.watchers["duration"]:
            logging.debug("[%s] Cancel duration timeout" % (self.id))
            self.watchers["duration"].stop()


    def init_timeout(self):
        if self.timeout > 0:
            self.watchers["timeout"] = pyev.Timer(self.timeout, 0.0, self.loop, self.timeout_cb)


    def set_timeout(self):
        logging.debug("[%s] Adding timeout: %s secs." % (self.id, self.timeout))

        if not self.watchers["timeout"]:
            self.init_timeout()
        else:
            self.watchers["timeout"].set(self.timeout, 0.0)

        self.watchers["timeout"].start()


    def cancel_timeout(self):
        if self.watchers["timeout"]:
            logging.debug("[%s] Cancel timeout" % (self.id))
            self.watchers["timeout"].stop()


    def __str__(self):
        return "<Probe: %s>" % self.id

