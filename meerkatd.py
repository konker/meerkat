#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# evtest
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#


import os
import sys

if sys.version < '2.6':
    sys.exit('Python 2.6 or 2.7 is required.')

import pathhack
import logging
from subprocess import Popen, PIPE
import signal
import pyev

# NOTE: edit config.rb as appropriate
from config.config import config
from storage.sqlite import Storage
import meerkat.probe


class Probe(object):
    def __init__(self, id, command, filters, interval, duration=-1, timeout=-1):
        self.id = id
        self.command = command
        self.filters = filters
        self.interval = interval
        self.duration = duration
        self.timeout = timeout
        self.watchers = {"timer": None, "io": None, "duration": None, "timeout": None}

    # execute the command
    def timer_cb(self, watcher, revents):
        logging.info(self.command)
        self.pipe = Popen(self.command, stdout=PIPE).stdout
        self.watchers["io"] = watcher.loop.io(self.pipe, pyev.EV_READ, self.io_cb)
        self.watchers["io"].start()

    # read any data available
    def io_cb(self, watcher, revents):
        logging.info('---- read----')
        logging.info(self.pipe.read())
        logging.info('----/read----')
        self.watchers["io"].stop()

    def register(self, loop):
        self.watchers["timer"] = loop.timer(0, self.interval, self.timer_cb)
        self.watchers["timer"].start()

        if self.duration > 0:
            self.watchers["duration"] = loop.timer(0, self.duration, self.duration_cb)
            self.watchers["duration"].start()

        if self.timeout > 0:
            self.watchers["timeout"] = loop.timer(0, self.timeout, self.timeout_cb)
            self.watchers["timeout"].start()

    def duration_cb(self, watcher, revents):
        # [FIXME: kill the subprocess?]
        pass

    def timeout_cb(self, watcher, revents):
        # [FIXME: kill the subprocess?]
        pass

    def stop(self):
        for k,w in self.watchers.items():
            if w:
                w.stop()


def main():
    loop = pyev.default_loop()

    # initialize and start a signal watcher
    sig = loop.signal(signal.SIGINT, signal_cb)
    sig.start()
    loop.data = [sig]

    # read in probes from config 
    for id, probe_conf in config["probes"].items():
        check_command(id, probe_conf)

        # load filters
        load_filters(id, probe_conf)
    
        p = get_probe(id, probe_conf)
        p.register(loop)
        loop.data.append(p)

    logging.info("Event loop start")
    loop.start()


def load_filters(id, probe_conf):
    if not "filters" in probe_conf:
        probe_conf["filters"] = []
        return

    # Dynamically load filters for the probe.
    # Replace the module/class name with an actual instance.
    for i, module in enumerate(probe_conf["filters"]):
        try:
            parts = module.split(".")
            cls = parts[-1]
            module = ".".join(parts[:-1])

            __import__(module, locals(), globals())
        except:
            # [FIXME]
            raise "ERROR0"

        if sys.modules.has_key(module):
            if hasattr(sys.modules[module], cls):
                probe_conf["filters"][i] = getattr(sys.modules[module], cls)()
            else:
                # [FIXME]
                raise "ERROR1"
        else:
            # [FIXME]
            raise "ERROR2"


def check_command(id, probe):
    # sanity check the probe command
    if not "command" in probe or len(probe["command"]) == 0:
        raise ValueError("Bad config: %s: missing or empty 'command' attribute" % id)

    if not type(probe["command"]) == type([]):
        raise ValueError("Bad config: %s: 'command' should be an array of strings" % id)

    # expand the command, saves doing this each time
    probe["command"][0] = os.path.join(config["probe_path"], probe["command"][0])
    

def get_probe(id, probe_conf):
    if not "type" in probe_conf:
        raise ValueError("Bad config: %s does not have a 'type' attribute" % id)

    if probe_conf["type"] == meerkat.probe.TYPE_DURATION:
        if not "interval" in probe_conf or not "duration" in probe_conf:
            raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute \
                              and a 'duration' attribute" % id)
        return Probe(id, probe_conf["command"], probe_conf["filters"], probe_conf["interval"], probe_conf["duration"])
    elif probe_conf["type"] == meerkat.probe.TYPE_PERIODIC:
        if not "interval" in probe_conf:
            raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute" % id)
        return Probe(id, probe_conf["command"], probe_conf["filters"], probe_conf["interval"])
    elif probe_conf["type"] == meerkat.probe.TYPE_CONTINUOUS:
        raise NotImplementedError("Probe type not yet implemented: %s" % probe_conf["type"])

    else:
        raise NotImplementedError("No such probe type: %s" % probe_conf["type"])

def signal_cb(watcher, revents):
    logging.info("SIGINT caught")
    loop = watcher.loop
    if loop.data:
        while loop.data:
            loop.data.pop().stop()

    loop.stop(pyev.EVBREAK_ALL)


if __name__ == '__main__':

    # configure logging
    logging.basicConfig(level=logging.DEBUG,
                        #filename=config['logfile'],
                        stream=sys.stdout,
                        format='%(asctime)s [%(threadName)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    main()


