# -*- coding: utf-8 -*-
#
# evtest
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import logging
from threading import Thread
import bottle
from bottle import template, static_file

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))

class HttpServer(object):
    def __init__(self, scheduler):
        self.scheduler = scheduler

        # set up the routes manually
        bottle.route('/static/<filepath:path>')(self.static)
        bottle.route("/")(self.index)


    def start(self):
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host='0.0.0.0', port='80'),
                                  name='http-thread')
        self.http_thread.setDaemon(True)
        self.http_thread.start()


    #### BOTTLE
    def index(self):
        return template('index', scheduler=self.scheduler)

    def static(self, filepath):
        return static_file(filepath, root=STATIC_ROOT)



