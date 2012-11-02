# -*- coding: utf-8 -*-
#
# meerkat.probe
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import logging
from subprocess import Popen, PIPE
import pyev


# constants
TYPE_DURATION = 1
TYPE_PERIODIC = 2
TYPE_CONTINUOUS = 4

DATA_TYPE_JSON = 8
DATA_TYPE_DATA = 16


class Probe(object):
    def __init__(self, id, storage, command, filters, error_filters, interval, duration=-1, timeout=-1):
        self.id = id
        self.storage = storage
        self.command = command
        self.filters = filters
        self.error_filters = error_filters
        self.interval = interval
        self.duration = duration
        self.timeout = timeout
        self.active = False
        self.last_error = None

        self.watchers = {
            "timer": None,
            "io": {
                "stdout": None,
                "stderr": None
            },
            "duration": None,
            "timeout": None
        }


    def register(self, loop):
        logging.info("Registered probe: %s" % self.id)
        self.watchers["timer"] = loop.timer(0, self.interval, self.timer_cb)
        self.watchers["timer"].start()


    # execute the command
    def timer_cb(self, watcher, revents):
        if self.active:
            logging.warning("%s: Interval callback when still in active state. Skipping" % self.id)
            return

        logging.debug(self.id)
        self.active = True
        self.process = Popen(self.command, stdout=PIPE, stderr=PIPE)

        if self.duration > 0:
            logging.debug("Adding duration timeout: %s secs." % self.duration)
            self.watchers["duration"] = watcher.loop.timer(self.duration, 0, self.duration_cb)
            self.watchers["duration"].start()

        if self.timeout > 0:
            logging.debug("Adding timeout: %s secs." % self.timeout)
            self.watchers["timeout"] = watcher.loop.timer(self.timeout, 0, self.timeout_cb)
            self.watchers["timeout"].start()

        self.watchers["io"]["stdout"] = watcher.loop.io(self.process.stdout, pyev.EV_READ, self.io_stdout_cb)
        self.watchers["io"]["stdout"].start()
        self.watchers["io"]["stderr"] = watcher.loop.io(self.process.stderr, pyev.EV_READ, self.io_stderr_cb)
        self.watchers["io"]["stderr"].start()


    # read any data available from stdout pipe
    def io_stdout_cb(self, watcher, revents):
        data = self.process.stdout.read()
        self.cancel_io()
        self.active = False

        for filter in self.filters:
            data = filter.filter(data)

        if self.storage:
            logging.debug("%s: -> %s" % (self.id, data))
            self.storage.write_str(self.id, data)


    # read any data available from stdout pipe
    def io_stderr_cb(self, watcher, revents):
        data = self.process.stderr.read()

        for filter in self.error_filters:
            data = filter.filter(data)

        # check that it is an error after filters
        if not data == '' and not data == None:
            logging.last_error = data
            logging.error("Error in probe: %s." % self.id)
            logging.debug(self.last_error)

            self.cancel_duration()
            self.cancel_timeout()
            self.cancel_io()
            self.active = False


    def kill_process(self):
        self.cancel_duration()
        self.cancel_timeout()
        try:
            self.process.kill()
        except OSError as ex:
            logging.error("Could not kill process: %s: %s" % (self.id, self.process.pid))

        self.active = False


    def duration_cb(self, watcher, revents):
        logging.debug("Duration complete: %s (%s secs.)" % (self.id, self.duration))
        self.kill_process()


    def timeout_cb(self, watcher, revents):
        logging.debug("Timeout complete: %s (%s secs.)" % (self.id, self.timeout))
        self.kill_process()


    def cancel_io(self):
        if self.watchers["io"]["stdout"]:
            self.watchers["io"]["stdout"].stop()
        if self.watchers["io"]["stderr"]:
            self.watchers["io"]["stderr"].stop()


    def cancel_duration(self):
        if self.watchers["duration"]:
            self.watchers["duration"].stop()


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

