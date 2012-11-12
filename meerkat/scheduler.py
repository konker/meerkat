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
from Queue import Queue, Empty

from meerkat.exception import MeerkatException
import meerkat.probe.probe as probe
from meerkat.processes.process import Process


COMMAND_EXEC = 1


class Scheduler(object):
    def __init__(self, probepath, processpath, probe_confs, storage, signal_cb):
        self.active = False
        self.active_probes = 0
        self.queue = Queue()

        self.probepath = probepath
        self.processpath = processpath
        def extra_signal_cb():
            signal_cb()

        self.extra_signal_cb = extra_signal_cb
        self.loop = pyev.Loop()

        # initialize and start a idle watcher
        idle_watcher = pyev.Idle(self.loop, self.idle_cb)
        idle_watcher.start()

        # initialize and start a signal watcher
        signal_watcher = pyev.Signal(signal.SIGINT, self.loop, self.sigint_cb)
        signal_watcher.start()

        self.loop.data = [idle_watcher, signal_watcher]

        # read in probes from config 
        self.probes = []
        index = 0
        for probe_conf in probe_confs:
            self.check_command(probe_conf)
            self.check_data_type(probe_conf)

            # load filters
            self.load_filters(probe_conf)

            # load error filters
            self.load_error_filters(probe_conf)

            # load post processes
            self.check_post_processes(probe_conf)
        
            p = self.get_probe(index, storage, probe_conf, -1)
            p.register(self.loop)
            self.probes.append(p)

            if probe_conf.get("auto_start", False):
                self.start_probe(index)

            index = index + 1


    def idle_cb(self, watcher, revents):
        if self.queue.empty():
            return

        try:
            command = self.queue.get_nowait()
        except Empty:
            command = None

        if command:
            if command[0] == COMMAND_EXEC:
                logging.debug("Idle: exec command: %s" % (command,))

                # pass the rest of the command elements as args to method
                getattr(self, command[1])(*command[2:])

            else:
                logging.debug("Idle: got unknown command: %s. Ignoring." % command)



    def sigint_cb(self, watcher, revents):
        logging.info("SIGINT caught. Exiting..")
        self.halt()
        self.extra_signal_cb()


    def start(self, paused=True):
        if not paused:
            self.start_probes()

        logging.info("Event loop start")
        self.loop.start()


    def start_probes(self):
        logging.info("Start all probes")
        for p in xrange(len(self.probes)):
            self.start_probe(p)


    def start_probe(self, p):
        logging.info("Start probe: %s" % self.probes[p].id)
        if not self.probes[p].running:
            self.active_probes = self.active_probes + 1
        self.probes[p].start()
        self.active = True


    def stop_probes(self):
        logging.info("Stop all probes")
        if self.probes:
            for p in xrange(len(self.probes)):
                self.stop_probe(p)


    def stop_probe(self, p):
        logging.info("Stop probe: %s" % self.probes[p].id)
        if self.probes[p].running:
            self.active_probes = self.active_probes - 1
        self.probes[p].stop()
        if self.active_probes == 0:
            self.active = False


    def halt(self):
        logging.info("Halting...")
        if self.loop.data:
            while self.loop.data:
                self.loop.data.pop().stop()

        if self.probes:
            self.stop_probes()

        self.loop.stop(pyev.EVBREAK_ALL)


    def check_post_processes(self, probe_conf):
        if not "post_processes" in probe_conf:
            probe_conf["post_processes"] = []
            return

        for i in xrange(len(probe_conf["post_processes"])):
            # expand the command
            probe_conf["post_processes"][i][0] = os.path.join(self.processpath, probe_conf["post_processes"][i][0])

            # instantite Process object
            probe_conf["post_processes"][i] = Process(probe_conf["post_processes"][i])


    def load_filters(self, probe_conf):
        self._load_filters(probe_conf, "filters")


    def load_error_filters(self, probe_conf):
        self._load_filters(probe_conf, "error_filters")


    def _load_filters(self, probe_conf, filter_conf_key):
        if not filter_conf_key in probe_conf:
            probe_conf[filter_conf_key] = []
            return

        # Dynamically load filters for then probe.
        # Replace the module/class name with an actual instance.
        for i, module in enumerate(probe_conf[filter_conf_key]):
            filter_id = module
            try:
                parts = module.split(".")
                cls = parts[-1]
                module = ".".join(parts[:-1])

                __import__(module, locals(), globals())
            except:
                raise MeerkatException("Could not import filter module: %s" % module)

            if sys.modules.has_key(module):
                if hasattr(sys.modules[module], cls):
                    probe_conf[filter_conf_key][i] = getattr(sys.modules[module], cls)(filter_id)
                else:
                    raise MeerkatException("Module %s has no class %s" % (module, cls))
            else:
                raise MeerkatException("Could not load filter module: %s" % module)


    def check_data_type(self, probe_conf):
        # sanity check the probe data type
        if not "data_type" in probe_conf \
            or not probe_conf["data_type"] in [probe.DATA_TYPE_TEXT, probe.DATA_TYPE_JSON, probe.DATA_TYPE_DATA]:
            raise ValueError("Bad config: %s: missing or invalid 'data_type' attribute" % probe_conf["id"])


    def check_command(self, probe_conf):
        # sanity check the probe command
        if not "command" in probe_conf or len(probe_conf["command"]) == 0:
            raise ValueError("Bad config: %s: missing or empty 'command' attribute" % probe_conf["id"])

        if not type(probe_conf["command"]) == type([]):
            raise ValueError("Bad config: %s: 'command' should be an array of strings" % probe_conf["id"])

        # expand the command, saves doing this each time
        probe_conf["command"][0] = os.path.join(self.probepath, probe_conf["command"][0])
        

    def get_probe(self, index, storage, probe_conf, timeout):
        # [FIXME: this is a bit dense]
        if not "type" in probe_conf:
            raise ValueError("Bad config: %s does not have a 'type' attribute" % probe_conf["id"])

        if probe_conf["type"] == probe.TYPE_DURATION:
            if not "interval" in probe_conf or not "duration" in probe_conf:
                raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute \
                                  and a 'duration' attribute" % probe_conf["id"])
            return probe.Probe(probe_conf["id"], index, storage, probe_conf, timeout)

        elif probe_conf["type"] == probe.TYPE_PERIODIC:
            if not "interval" in probe_conf:
                raise ValueError("Bad config: %s: probes of this type must have a 'interval' attribute" % probe_conf["id"])
            probe_conf["duration"] = -1
            return probe.Probe(probe_conf["id"], index, storage, probe_conf, timeout)

        elif probe_conf["type"] == probe.TYPE_CONTINUOUS:
            raise NotImplementedError("Probe type not yet implemented: %s" % probe_conf["type"])

        else:
            raise NotImplementedError("No such probe type: %s" % probe_conf["type"])

