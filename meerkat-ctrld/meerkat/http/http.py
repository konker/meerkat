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
from threading import Thread
import json
import socket
import requests
import bottle
from bottle import template, static_file, request, response

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


class HttpServer(object):
    def __init__(self, config):
        self.host = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host)
        self.nodes = {}
        self.config = config

        # set up the routes manually
        #bottle.route('/static/<filepath:path>', method='GET')(self.static)
        #bottle.route('/', method='GET')(self.index)
        bottle.route('/meerkat/nodes.json', method='GET')(self.nodes_json)
        bottle.route('/meerkat/node.json', method='GET')(self.node_json)
        bottle.route('/meerkat/register.json', method='POST')(self.register_control)
        bottle.route('/meerkat/log.json', method='GET')(self.log_json)


    def start(self):
        bottle.run(host='0.0.0.0', port=9300, server='cherrypy', debug=False, quiet=True)
        logging.info("Http control server started.")


    def node_json(self):
        id = request.query.id

        ret = {"status": "OK",
                "body": None
        }

        try:
            logging.info("Fetching: %s", self.nodes[id]["info"]["info_url"])
            r = requests.get(self.nodes[id]["info"]["info_url"], verify=False)
            ret["body"] = r.text
            logging.info("Fetched: %s", r.text)
        except Exception as ex:
            ret["status"] = "ERROR"
            ret["body"] = str(ex)

        return json.dumps(ret)


    def nodes_json(self):
        ret = {"status": "OK",
                "body": {
                    "nodes": self.nodes
              }
        }
        return json.dumps(ret)


    def register_control(self):
        node = request.body.read()
        try:
            node = json.loads(node)

            if node.get("status", False):
                node = node["body"]

            self.nodes[node["id"]] = node
            logging.info("Registered node: %s", node["id"])
        except ValueError as ex:
            ret = {"status": "ERROR", "body": str(ex)}
            logging.info(str(ex))
            return json.dumps(ret)

        ret = {"status": "OK", "body": ""}
        return json.dumps(ret)


    def log_json(self):
        lines = request.query.n or 10
        stdin,stdout = os.popen2("tail -n %s %s" % (lines, self.config['logfile']))
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


    '''
    def static(self, filepath):
        if 'latest' in filepath:
            response.set_header('Cache-Control', 'No-store')

        return static_file(filepath, root=STATIC_ROOT)
    '''




