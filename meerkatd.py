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
import daemon

# NOTE: edit config.rb as appropriate
from config.config import config
from meerkat.scheduler import Scheduler
from meerkat.http.http import HttpServer
from util.pidfile import PidFile


def main():
    parser = OptionParser()

    parser.add_option('--debug', action='store_true', default=False,
                      help='log debugging messages too')

    parser.add_option('--log-stderr', dest='log_stderr',
                      action='store_true', default=False,
                      help='force log messages to stderr')

    parser.add_option('--foreground', '-f', dest='foreground',
                      action='store_true', default=False,
                      help='do not run as daemon')

    options, args = parser.parse_args()
    if args:
        parser.error('incorrect number of arguments')

    if options.foreground:
        meerkatd(options)
    else:
        # NOTE: the pidfile path must be the same as $PIDFILE in the init.d script
        with daemon.DaemonContext(pidfile=PidFile('/var/run/meerkatd.pid')):
            meerkatd(options)


def meerkatd(options):
    # configure logging
    if options.debug or config.get('debug', False):
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

    # initialize the scheduler
    scheduler = Scheduler(config["datafile"], config["probespath"], config["probes"])

    # start http server
    http_server = HttpServer(scheduler, config)
    http_server.start()

    # register with mission control
    #r = requests.post(config["mission_control"]["register_url"], data=http_server.info_json())
    r = http_server.register_control_json()
    logging.info("Registered with mission control: %s" % r)

    # start the scheduler
    scheduler.start(paused=True)


if __name__ == '__main__':
    main()


