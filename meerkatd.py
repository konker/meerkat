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

# NOTE: edit config.rb as appropriate
from config.config import config
from storage.sqlite import Storage
from meerkat.scheduler import Scheduler
from meerkat.http.http import HttpServer


def main():
    # configure logging
    logging.basicConfig(level=logging.DEBUG,
                        #filename=config['logfile'],
                        stream=sys.stdout,
                        format='%(asctime)s [%(threadName)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # initialize storage
    storage = Storage(config["datafile"])

    def signal_cb():
        storage.close()

    # initialize the scheduler
    scheduler = Scheduler(config["probe_path"], config["probes"], storage, signal_cb)

    # start http server
    http_server = HttpServer(scheduler)
    http_server.start()

    # start the scheduler
    scheduler.start()


if __name__ == '__main__':
    main()


