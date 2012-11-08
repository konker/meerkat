# -*- coding: utf-8 -*-
#
# meerkat.probe.probe
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import fcntl
import logging
from subprocess import Popen, PIPE
from threading import RLock
import pyev


# constants
TYPE_DURATION = 1
TYPE_PERIODIC = 2
TYPE_CONTINUOUS = 4

DATA_TYPE_JSON = 8
DATA_TYPE_TEXT = 16
DATA_TYPE_DATA = 32


class Probe(object):
    def __init__(self, id, index, storage, probe_conf, timeout=-1): #command, data_type, filters, error_filters, interval, duration=-1, timeout=-1):
        self.id = id
        self.index = index
        self.storage = storage
        self.command = probe_conf["command"]
        self.data_type = probe_conf["data_type"]
        self.filters = probe_conf["filters"]
        self.error_filters = probe_conf["error_filters"]
        self.interval = probe_conf["interval"]
        self.duration = probe_conf["duration"]
        self.timeout = timeout
        self.active = False
        self.running = False
        self.last_error = None
        self.loop = None
        self.process = None
        self.buf = None
        self.err_buf = None
        self.lock = RLock()

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
        logging.info("Registered probe: %s" % self.id)


    def start(self):
        self.set_interval()
        self.running = True


    def stop(self, watchers=None):
        if watchers == None:
            watchers = self.watchers

        for k,w in watchers.items():
            if w:
                if type(w) == type({}):
                    # recurse
                    self.stop(w)
                else:
                    w.stop()

        self.active = False
        self.running = False


    # execute the command
    def interval_cb(self, watcher, revents):
        logging.debug("[%s] Interval complete: %s secs." % (self.id, self.interval))

        if self.active:
            logging.warning("[%s] Interval callback when still in active state. Skipping" % self.id)
            return

        self.active = True
        self.cancel_interval()

        # create a sub-process for the probe command, listen to stdout and stderr
        self.process = Popen(self.command, bufsize=0, shell=True, stdout=PIPE, stderr=PIPE)
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
        logging.debug("[%s] Stdout ready" % self.id)
        self.make_nonoblocking(self.process.stdout)

        data = self.process.stdout.read()

        # process the data and re-start the interval
        # if not waiting for a duration
        if self.duration < 0:
            # cancel outstanding watchers
            self.cancel_all()

            self.process_data(data)
            self.last_error = None

            self.active = False
            self.set_interval()
        else:
            if data == '':
                # EOF
                self.cancel_io()
            else:
                self.buf.append(data)


    # read any data available from stderr pipe
    def io_stderr_cb(self, watcher, revents):
        logging.debug("[%s] Stderr ready" % self.id)
        # [XXX: if blocking, wifi_scan blocks the event loop,
        # but others will only get the first line of stack trace?
        # Pos. have err_buf like stdout buf and collect stderr before processing?]
        self.make_nonoblocking(self.process.stderr)

        # read in error data
        error = self.process.stderr.read()

        if self.duration < 0:
            error = self.process_error(error)
            if self.is_error(error):
                self.handle_error(error)
        else:
            if error == '':
                # EOF
                error = self.process_error(self.err_buf)
                if self.is_error(error):
                    self.handle_error(error)
            else:
                self.err_buf.append(error)


    def handle_error(self, error):
        self.last_error = error
        logging.error("Error in probe: %s: %s" % (self.id, self.last_error))

        # cancel outstanding watchers
        self.cancel_all()

        # start the interval again
        self.active = False
        self.set_interval()


    def is_error(self, error):
        return (error != '' and error != None)


    def duration_cb(self, watcher, revents):
        logging.debug("[%s] Duration complete: %s secs." % (self.id, self.duration))

        # cancel outstanding watchers
        self.cancel_all()

        # terminate the current process
        self.terminate_process()

        # check for error
        error = self.process_error(self.err_buf)
        if self.is_error(error):
            self.handle_error(error)
        else:
            # OK - deal with the collected data
            self.last_error = None
            self.process_data(self.buf)

            # start the interval again
            self.active = False
            self.set_interval()


    def timeout_cb(self, watcher, revents):
        logging.debug("[%s] Timeout complete %s secs." % (self.id, self.timeout))

        # cancel outstanding watchers
        self.cancel_all()

        # kill the current process
        self.kill_process()

        # check for error
        error = self.process_error(self.err_buf)
        if self.is_error(error):
            self.handle_error(error)
        else:
            # OK - deal with the collected data
            self.last_error = None
            self.process_data(self.buf)

            # start the interval again
            self.active = False
            self.set_interval()


    # set the given pipe to be in non-blocking mode
    def make_nonoblocking(self, pipe):
        fd = pipe.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


    # terminate the process SIGTERM
    def terminate_process(self):
        try:
            self.process.terminate()
        except OSError as ex:
            logging.error("Could not terminate process: %s: %s" % (self.id, self.process.pid))


    # kill the process SIGKILL
    def kill_process(self):
        try:
            self.process.kill()
        except OSError as ex:
            logging.error("Could not terminate process: %s: %s" % (self.id, self.process.pid))


    def process_error(self, error):
        # deal with a buffer
        if type(error) == list:
            error = ''.join(error)

        # apply error filters
        for filter in self.error_filters:
            error = filter.filter(error)

        self.last_error = error
        return error


    def process_data(self, data):
        # deal with a buffer
        if type(data) == list:
            if self.data_type == DATA_TYPE_JSON:
                # XXX: bit of a hack
                if len(data) == 1 and data[0].startswith('['):
                    data = data[0]
                else:
                    data = '[' + ','.join(data) + ']'
            elif self.data_type == DATA_TYPE_TEXT:
                # [FIXME: do we need this?]
                data = ''.join(data)
            else:
                data = b''.join(data)

        # apply filters
        for filter in self.filters:
            # 1) maintain a filter pointer
            # 2) only write to storage if filter pointer is END
            # 3) apply the current filter and increment pointer
            # - separate above data pre-processing from  filter application?
            # - storage also separate
            # - proc filters:
            #   - do we use the same loop?
            #       - if so, extra watchers needed
            data = filter.filter(data)

        # store
        if self.storage:
            logging.debug("[%s] -> %s" % (self.id, data))
            self.storage.write_str(self.id, data)


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
            logging.debug("[%s] Cancel interval" % self.id)
            self.watchers["interval"].stop()


    def init_io_stdout(self):
        self.watchers["io"]["stdout"] = pyev.Io(self.process.stdout, pyev.EV_READ, self.loop, self.io_stdout_cb)


    def init_io_stderr(self):
        self.watchers["io"]["stderr"] = pyev.Io(self.process.stderr, pyev.EV_READ, self.loop, self.io_stderr_cb)


    def set_io(self):
        logging.debug("[%s] Adding I/O watchers" % self.id)

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
        if self.watchers["io"]["stdout"]:
            logging.debug("[%s] Cancel stdout I/O watcher" % self.id)
            self.watchers["io"]["stdout"].stop()
        if self.watchers["io"]["stderr"]:
            logging.debug("[%s] Cancel stderr I/O watcher" % self.id)
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
            logging.debug("[%s] Cancel duration timeout" % self.id)
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
            logging.debug("[%s] Cancel timeout" % self.id)
            self.watchers["timeout"].stop()


    def __str__(self):
        return "<Probe: %s>" % self.id

