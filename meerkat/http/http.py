# -*- coding: utf-8 -*-
#
# meerkat.http.http
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import time
import logging
from datetime import timedelta
from threading import Thread
import json
import socket
import bottle
from bottle import template, static_file, request, response

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


class HttpServer(object):
    def __init__(self):
        self.host = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host)
        self.nodes = {}

        # set up the routes manually
        bottle.route('/static/<filepath:path>', method='GET')(self.static)
        bottle.route('/', method='GET')(self.index)
        bottle.route('/nodes.json', method='GET')(self.nodes_json)
        bottle.route('/register/', method='POST')(self.register_control)
        bottle.route('/log.json', method='GET')(self.log_json)


    def start(self):
        '''
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host='0.0.0.0', port=8080, server='cherrypy', debug=False, quiet=True),
                                  name='http-thread')
        self.http_thread.setDaemon(True)
        self.http_thread.start()
        '''
        bottle.run(host='0.0.0.0', port=8080, server='cherrypy', debug=False, quiet=True)
        logging.info("Http control server started.")


    def index(self):
        return template('index')
    

    def nodes_json(self):
        ret = {"status": "OK",
                "body": {
                    "nodes": self.nodes
              }
        }
        return json.dumps(ret)


    def register_control(self):
        node = request.body
        try:
            node = json.loads(node)
        except ValueError as ex:
            pass

        self.nodes[node["id"]] = node

        ret = {"status": "OK"}
        return json.dumps(ret)


    def log_json(self):
        lines = request.query.n or 10
        stdin,stdout = os.popen2("tail -n %s %s" % (lines, 'meerkat-ctrld.log'))
        stdin.close()
        log = stdout.readlines()
        stdout.close()

        ret = {"status": "OK",
               "body": {
                    "log": log,
                }
              }

        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)  


    def static(self, filepath):
        if 'latest' in filepath:
            response.set_header('Cache-Control', 'No-store')

        return static_file(filepath, root=STATIC_ROOT)




