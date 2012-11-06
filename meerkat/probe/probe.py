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
import pyev


# constants
TYPE_DURATION = 1
TYPE_PERIODIC = 2
TYPE_CONTINUOUS = 4

DATA_TYPE_JSON = 8
DATA_TYPE_TEXT = 16
DATA_TYPE_DATA = 32


class Probe(object):
    def __init__(self, id, index, storage, command, data_type, filters, error_filters, interval, duration=-1, timeout=-1):
        self.id = id
        self.index = index
        self.storage = storage
        self.command = command
        self.data_type = data_type
        self.filters = filters
        self.error_filters = error_filters
        self.interval = interval
        self.duration = duration
        self.timeout = timeout
        self.active = False
        self.running = False
        self.last_error = None
        self.loop = None
        self.buf = None

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
        logging.info("Registered probe: %s" % self.id)


    def start(self):
        self.init_interval()
        self.running = True


    # execute the command
    def interval_cb(self, watcher, revents):
        logging.debug("Interval complete: %s (%s secs.)" % (self.id, self.interval))

        if self.active:
            logging.warning("%s: Interval callback when still in active state. Skipping" % self.id)
            return

        self.active = True
        self.cancel_interval()

        # create a sub-process for the probe command, listen to stdout and stderr
        self.process = Popen(self.command, bufsize=0, shell=True, stdout=PIPE, stderr=PIPE)
        self.buf = []

        # initialize I/O watchers
        self.init_io()

        # set up a watcher to kill the process after the duration
        if self.duration > 0:
            self.init_duration()

        # set up a watcher to kill the process after a global timeout
        if self.timeout > 0:
            self.init_timeout()


    # read any data available from stdout pipe
    def io_stdout_cb(self, watcher, revents):
        logging.debug("Stdout ready: %s." % self.id)
        self.set_nonoblocking(self.process.stdout)

        data = self.process.stdout.read()

        # process the data and re-start the interval
        # if not waiting for a duration
        if self.duration < 0:
            # cancel outstanding watchers
            self.cancel_all()

            self.process_data(data)
            self.last_error = None

            self.active = False
            self.init_interval()
        else:
            # EOF
            if data == '':
                self.cancel_io()
            else:
                self.buf.append(data)


    # read any data available from stderr pipe
    def io_stderr_cb(self, watcher, revents):
        logging.debug("Stderr ready: %s." % self.id)
        #self.set_nonoblocking(self.process.stderr)

        # read in error data
        data = self.process.stderr.read()

        # apply error filters
        for filter in self.error_filters:
            data = filter.filter(data)

        # check that it is an error after filters
        if not data == '' and not data == None:
            self.last_error = data
            logging.error("Error in probe: %s: %s" % (self.id, self.last_error))

            # cancel outstanding watchers
            self.cancel_all()

            # start the interval again
            self.active = False
            self.init_interval()


    def duration_cb(self, watcher, revents):
        logging.debug("Duration complete: %s (%s secs.)" % (self.id, self.duration))

        # cancel outstanding watchers
        self.cancel_all()

        # terminate the current process
        self.terminate_process()

        # deal with the collected data
        self.process_data(self.buf)
        self.last_error = None

        # start the interval again
        self.active = False
        self.init_interval()


    def timeout_cb(self, watcher, revents):
        logging.debug("Timeout complete: %s (%s secs.)" % (self.id, self.timeout))

        # cancel outstanding watchers
        self.cancel_all()

        # kill the current process
        self.kill_process()

        # deal with the collected data
        self.process_data(self.buf)

        # start the interval again
        self.active = False
        self.init_interval()


    # set the given pipe to be in non-blocking mode
    def set_nonoblocking(self, pipe):
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


    def process_data(self, data):
        # deal with a buffer
        '''
        print "processing data:"
        print self.id
        print type(data)
        print data
        '''
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
            data = filter.filter(data)

        # store
        if self.storage:
            logging.debug("%s: -> %s" % (self.id, data))
            self.storage.write_str(self.id, data)


    def cancel_all(self):
        self.cancel_timeout()
        self.cancel_duration()
        self.cancel_io()
        self.cancel_interval()


    def init_interval(self):
        logging.debug("Adding interval timer for %s. (%s secs)" % (self.id, self.interval))

        if not self.watchers["interval"]:
            self.watchers["interval"] = pyev.Timer(self.interval, 0.0, self.loop, self.interval_cb)
        else:
            self.watchers["interval"].set(self.interval, 0.0)

        self.watchers["interval"].start()


    def cancel_interval(self):
        if self.watchers["interval"]:
            self.watchers["interval"].stop()


    def init_io(self):
        logging.debug("Adding I/O watchers for %s." % self.id)

        # set up watchers for stdout
        if not self.watchers["io"]["stdout"]:
            self.watchers["io"]["stdout"] = pyev.Io(self.process.stdout, pyev.EV_READ, self.loop, self.io_stdout_cb)
        else:
            self.watchers["io"]["stdout"].set(self.process.stdout, pyev.EV_READ)

        self.watchers["io"]["stdout"].start()

        # set up watchers for stderr
        if not self.watchers["io"]["stderr"]:
            self.watchers["io"]["stderr"] = pyev.Io(self.process.stderr, pyev.EV_READ, self.loop, self.io_stderr_cb)
        else:
            self.watchers["io"]["stderr"].set(self.process.stderr, pyev.EV_READ)

        self.watchers["io"]["stderr"].start()


    def cancel_io(self):
        if self.watchers["io"]["stdout"]:
            self.watchers["io"]["stdout"].stop()
        if self.watchers["io"]["stderr"]:
            self.watchers["io"]["stderr"].stop()


    def init_duration(self):
        logging.debug("Adding duration timeout: %s secs." % self.duration)

        if not self.watchers["duration"]:
            self.watchers["duration"] = pyev.Timer(self.duration, 0.0, self.loop, self.duration_cb)
        else:
            self.watchers["duration"].set(self.duration, 0.0)

        self.watchers["duration"].start()


    def cancel_duration(self):
        if self.watchers["duration"]:
            self.watchers["duration"].stop()


    def init_timeout(self):
        logging.debug("Adding timeout: %s secs." % self.timeout)

        if not self.watchers["timeout"]:
            self.watchers["timeout"] = pyev.Timer(self.timeout, 0.0, self.loop, self.timeout_cb)
        else:
            self.watchers["timeout"].set(self.timeout, 0.0)

        self.watchers["timeout"].start()


    def cancel_timeout(self):
        if self.watchers["timeout"]:
            self.watchers["timeout"].stop()


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


    def __str__(self):
        return "<Probe: %s>" % self.id
