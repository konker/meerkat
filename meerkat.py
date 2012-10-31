#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#


"""
TODO:
    - meerkat.probes package holds small stand-alone probe programs
        - each probe writes JSON/binary data(?) to it's stdout
        - can be called from command line
        - each probe can take some standard arguments:
            --duration-secs=n
            - is it the probe's responsibility to manage duration?
                - or should the master program terminate a probe after n secs?
                    - what about data in inconsisitent state?


        - do we need a Probe base class?

    - probes are configured by config.config
        "global_filters": [
            # or just repeat this in each filters array?
            # XXX: does this imply that all probes have BINARY data_type?
            "meerkat.filter.ecrypt"
        ],
        - "probes": [
            "meerkat.probe.bluetooth": {
                "type": "PROBE_DURATION",
                "duration": 30,
                "delay": 60,
                "data_type": "JSON",
                "filters": [
                    "meerkat.filter.drop_unchanged"
                ]
            },
            "meerkat.probe.wifi_scan": {
                "type": "PROBE_PERIODIC",
                "delay": 30,
                "data_type": "JSON",
                "filters": [
                    "meerkat.filter.drop_unchanged"
                ]
            },
            "meerkat.probe.wifi_fake_ap": {
                "type": "PROBE_CONTINUOUS",
                "data_type": "JSON"
            },
            "meerkat.probe.wifi_packet_sniff": {
                "type": "PROBE_DURATION",
                "duration": 30,
                "delay": 30,
                "data_type": "JSON",
                "filters": [
                    "meerkat.filter.packet_filter"
                ]
            },
            "meerkat.probe.photo": {
                "type": "PROBE_PERIODIC",
                "delay": 30,
                "data_type": "JSON", # this matches the output of all filters
                "filters": [
                    "meerkat.filter.opencv_pedestrian_count"
                ]
            }
        ]

    - main program loads and manages each probe
        - responsible for scheduling probe calls:
            - DURATION: run for a duration of y secs with a delay for x secs
            - PERIODIC: run every x secs
                - this the same as DURATION, but with a duration of -1 => until exit
            - CONTINUOUS: run and continuously read data
                - e.g. video stream,
                - e.g. fake wifi ap
        - probes are called using multiprocessing with pipes for probe stdout
        - event loop for reading on file descriptors?
            - pyev

    - main program provides storage
        - sqlite
        - pos. encrypt

    - main program manages filters
        - plugins loaded from meerkat.filters
        - filters provide a filter(data) method
        - config.config configures which filters are applied to which probes
        - could be multiple filters pipelined for one probe
        - e.g. photo try and detect faces, send that meta-data,
          drop actual photo
        - maybe encryption could be a fitler?
            - a way to configure 'global' filters that automatically apply
              to all probes?
        - do we need a Filter base class?

    - proposed probes:
        - wifi ap scan
        - wifi packet scan
        - fake wifi ap
        - bluetooth device scan
        - periodic photo
            - video stream => very small delay (?)

    - proposed filters:
        - encrytion
        - packet sniff grep filter, e.g. tcp port 80, get host
        - opencv based "pedestrian detect" filter
        - drop if unchanged filter (?)

    - http ui:
        - bottle
            - or is this better done in nodejs?
                - can we have the access that we need across py/nodejs?
        - websockets possibly?
            - https://github.com/zeekay/bottle-websocket
            - socket.io in nodejs
        - show the latest data
            - latest picture captured
        - timeline ui of some kind?
        - show status
            - probes configured
            - probes currently running
            - filters?
        - start/stop system?

    - what about:
        - Motion?

    - potential problems:
        - wifi dongle no moitor mode: cannot do packet sniffing
            - pos. re-compile kernel?
        - when wifi dongle is in monitor mode for sniffing
            - cannot do wifi scan?
                - sniffing => wifi scan?
            - cannot do fake AP?
        - usb storage drive draws too much power?
            - use bigger sdhc card?
        - general performance problems
            - use netbook?
        - opencv on arm?
            - seems python-opencv package is available



"""
import os
import sys

if sys.version < '2.5':                                                               
    sys.exit('Python 2.5 or 2.6 is required.')  

import pathhack

import logging
from threading import Thread
from subprocess import Popen, PIPE
from kronos import Scheduler, method

# NOTE: edit config.rb as appropriate
from config.config import config

import meerkat.probe

FILTER_PACKAGE = 'meerkat.filters'
FILTER_CLASS = 'Filter'

scheduler = Scheduler()


def main():
    # read in probes from config 
    for id, probe in config["probes"].items():
        check_command(id, probe)

        # load filters
        load_filters(id, probe)

        # schedule/start
        schedule(id, probe)

        #print id, probe


def make_schedule_function(id, command, filters):
    def _func():
        #print command
        pipe = Popen(command, stdout=PIPE).stdout
        data = pipe.read()
        for filter in filters:
            data = filter.filter(data)

        print id, " -> ", data

    return _func


def schedule(id, probe):
    if not "type" in probe:
        raise ValueError("Bad config: %s does not have a 'type' attribute" % id)

    if probe["type"] == meerkat.probe.TYPE_DURATION:
        print "TYPE_DURATION"
        if not "delay" in probe or not "duration" in probe:
            raise ValueError("Bad config: %s: probes of this type must have a 'delay' attribute \
                              and a 'duration' attribute" % id)
        make_schedule_function(id, probe["command"], probe["filters"])()
        '''
        scheduler.add_interval_task(
                make_schedule_function(id, probe["command"], probe["filters"]),
                id,
                0,
                probe["delay"],
                method.sequential, None, None)
        '''
    elif probe["type"] == meerkat.probe.TYPE_PERIODIC:
        print "TYPE_PERIODIC"
        if not "delay" in probe:
            raise ValueError("Bad config: %s: probes of this type must have a 'delay' attribute" % id)
        make_schedule_function(id, probe["command"], probe["filters"])()
        '''
        scheduler.add_interval_task(
                make_schedule_function(id, probe["command"], probe["filters"]),
                id,
                0,
                probe["delay"],
                method.sequential, None, None)
        '''
    elif probe["type"] == meerkat.probe.TYPE_CONTINUOUS:
        print "TYPE_CONTINUOUS"
        make_schedule_function(id, probe["command"])()
    else:
        raise NotImplementedError("No such probe type: %s" % probe["type"])


def load_filters(id, probe):
    if not "filters" in probe:
        probe["filters"] = []
        return

    # Dynamically load filters for the probe.
    # Replace the module/class name with an actual instance.
    for i, module in enumerate(probe["filters"]):
        try:
            parts = module.split(".")
            cls = parts[-1]
            module = ".".join(parts[:-1])

            __import__(module, locals(), globals())
        except:
            raise "ERROR0"

        if sys.modules.has_key(module):
            if hasattr(sys.modules[module], cls):
                probe["filters"][i] = getattr(sys.modules[module], cls)()
            else:
                raise "ERROR1"
        else:
            raise "ERROR2"


def check_command(id, probe):
    # sanity check the probe command
    if not "command" in probe or len(probe["command"]) == 0:
        raise ValueError("Bad config: %s: missing or empty 'command' attribute" % id)

    if not type(probe["command"]) == type([]):
        raise ValueError("Bad config: %s: 'command' should be an array of strings" % id)

    # expand the command, saves doing this each time
    probe["command"][0] = os.path.join(config["probe_path"], probe["command"][0])



if __name__ == '__main__':

    # configure logging
    logging.basicConfig(level=logging.DEBUG,
                        #filename=config['logfile'],
                        stream=sys.stdout,
                        format='%(asctime)s [%(threadName)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    main()

