#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# evtest
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys

if sys.version < '2.7':
    sys.exit('Python 2.7 is required.')

import pathhack
import logging
from optparse import OptionParser

# NOTE: edit config.rb as appropriate
from config.config import config
from storage.sqlite import Storage
from meerkat.scheduler import Scheduler
from meerkat.http.http import HttpServer


def main():
    parser = OptionParser()

    parser.add_option('--debug', action='store_true', default=False,
                      help='log debugging messages too')

    parser.add_option('--log-stderr', dest='log_stderr',
                      action='store_true', default=False,
                      help='force log messages to stderr')

    options, args = parser.parse_args()
    if args:
        parser.error('incorrect number of arguments')

    # configure logging
    if options.debug:
        if options.log_stderr:
            logging.basicConfig(level=logging.DEBUG,
                                stream=sys.stderr,
                                format='%(asctime)s [%(threadName)s] %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(level=logging.DEBUG,
                                filename=config['logfile'],
                                format='%(asctime)s [%(threadName)s] %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
    else:
        if options.log_stderr:
            logging.basicConfig(level=logging.INFO,
                                stream=sys.stderr,
                                format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(level=logging.INFO,
                                filename=config['logfile'],
                                format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

    # initialize storage
    storage = Storage(config["datafile"])

    def signal_cb():
        storage.close()

    # initialize the scheduler
    scheduler = Scheduler(config["probe_path"], config["probes"], storage, signal_cb)

    # start http server
    http_server = HttpServer(scheduler, config)
    http_server.start()

    # start the scheduler
    scheduler.start(paused=True)


if __name__ == '__main__':
    main()


