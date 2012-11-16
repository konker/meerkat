#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# meerkat-ctrld
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys

import pathhack
import logging
from optparse import OptionParser

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
                                filename='meerkat-ctrld.log',
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
                                filename='meerkat-ctrld.log',
                                format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

    # start http server
    http_server = HttpServer()
    http_server.start()


if __name__ == '__main__':
    main()


