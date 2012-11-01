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
import signal
import pyev

# NOTE: edit config.rb as appropriate
from config.config import config
from storage.sqlite import Storage
import meerkat.probe


def main():
    storage = storage.sqlite.Storage(config["datafile"])

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
    
        p = get_probe(id, probe_conf, storage)
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
            raise MeerkatException("Could not import filter module: %s" % module)

        if sys.modules.has_key(module):
            if hasattr(sys.modules[module], cls):
                probe_conf["filters"][i] = getattr(sys.modules[module], cls)()
            else:
                raise MeerkatException("Module %s has no class %s" % (module, cls))
        else:
            raise MeerkatException("Could not load filter module: %s" % module)


def check_command(id, probe):
    # sanity check the probe command
    if not "command" in probe or len(probe["command"]) == 0:
        raise ValueError("Bad config: %s: missing or empty 'command' attribute" % id)

    if not type(probe["command"]) == type([]):
        raise ValueError("Bad config: %s: 'command' should be an array of strings" % id)

    # expand the command, saves doing this each time
    probe["command"][0] = os.path.join(config["probe_path"], probe["command"][0])
    

def get_probe(id, probe_conf, storage):
    if not "type" in probe_conf:
        raise ValueError("Bad config: %s does not have a 'type' attribute" % id)

    if probe_conf["type"] == meerkat.probe.TYPE_DURATION:
        if not "interval" in probe_conf or not "duration" in probe_conf:
            raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute \
                              and a 'duration' attribute" % id)
        return meerkat.probe.Probe(id, storage, probe_conf["command"], probe_conf["filters"], probe_conf["interval"], probe_conf["duration"])
    elif probe_conf["type"] == meerkat.probe.TYPE_PERIODIC:
        if not "interval" in probe_conf:
            raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute" % id)
        return meerkat.probe.Probe(id, storage, probe_conf["command"], probe_conf["filters"], probe_conf["interval"])
    elif probe_conf["type"] == meerkat.probe.TYPE_CONTINUOUS:
        raise NotImplementedError("Probe type not yet implemented: %s" % probe_conf["type"])

    else:
        raise NotImplementedError("No such probe type: %s" % probe_conf["type"])


def signal_cb(watcher, revents):
    logging.info("SIGINT caught. Exiting..")
    loop = watcher.loop
    if loop.data:
        while loop.data:
            loop.data.pop().stop()

    loop.stop(pyev.EVBREAK_ALL)


if __name__ == '__main__':

    # configure logging
    logging.basicConfig(level=logging.INFO,
                        #filename=config['logfile'],
                        stream=sys.stdout,
                        format='%(asctime)s [%(threadName)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    main()


