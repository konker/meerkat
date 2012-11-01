# -*- coding: utf-8 -*-
#
# meerkat.scheduler
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import sys
import logging
import signal
import pyev

import meerkat.probe


class Scheduler(object):
    def __init__(self, probe_path, probe_confs, storage, signal_cb):
        self.probe_path = probe_path
        def extra_signal_cb():
            signal_cb()

        self.extra_signal_cb = extra_signal_cb
        self.loop = pyev.default_loop()

        # initialize and start a signal watcher
        sig = self.loop.signal(signal.SIGINT, self.sigint_cb)
        sig.start()
        self.loop.data = [sig]

        # read in probes from config 
        self.probes = []
        for id, probe_conf in probe_confs.items():
            self.check_command(id, probe_conf)

            # load filters
            self.load_filters(id, probe_conf)
        
            p = self.get_probe(id, probe_conf, storage)
            p.register(self.loop)
            self.probes.append(p)


    def sigint_cb(self, watcher, revents):
        logging.info("SIGINT caught. Exiting..")
        self.stop()
        self.extra_signal_cb()


    def start(self):
        logging.info("Event loop start")
        self.loop.start()


    def stop(self):
        if self.loop.data:
            while self.loop.data:
                self.loop.data.pop().stop()

        if self.probes:
            while self.probes:
                self.probes.pop().stop()

        self.loop.stop(pyev.EVBREAK_ALL)


    def load_filters(self, id, probe_conf):
        if not "filters" in probe_conf:
            probe_conf["filters"] = []
            return

        # Dynamically load filters for then probe.
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


    def check_command(self, id, probe_conf):
        # sanity check the probe command
        if not "command" in probe_conf or len(probe_conf["command"]) == 0:
            raise ValueError("Bad config: %s: missing or empty 'command' attribute" % id)

        if not type(probe_conf["command"]) == type([]):
            raise ValueError("Bad config: %s: 'command' should be an array of strings" % id)

        # expand the command, saves doing this each time
        probe_conf["command"][0] = os.path.join(self.probe_path, probe_conf["command"][0])
        

    def get_probe(self, id, probe_conf, storage):
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

