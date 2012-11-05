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
from datetime import timedelta
from threading import Thread
import json
import socket
import bottle
from bottle import template, static_file, request
from storage.sqlite import Storage

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))

class HttpServer(object):
    def __init__(self, scheduler, config):
        self.scheduler = scheduler
        self.config = config
        self.storage = None

        self.host = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host)

        # set up the routes manually
        bottle.route('/static/<filepath:path>', method='GET')(self.static)
        bottle.route('/', method='GET')(self.index)
        bottle.route('/master.json', method='GET')(self.master_json)
        bottle.route('/master.json', method='POST')(self.master_control_json)
        bottle.route('/probes.json', method='GET')(self.probes_json)
        bottle.route('/probe<p:int>.json', method='GET')(self.probe_json)
        bottle.route('/probe<p:int>.json', method='POST')(self.probe_control_json)
        bottle.route('/log.json', method='GET')(self.log_json)


    def start(self):
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host=self.config['http_host'], port=self.config['http_port']),
                                  name='http-thread')
        self.http_thread.setDaemon(True)
        self.http_thread.start()


    def index(self):
        if not self.storage:
            self.storage = Storage(self.config['datafile'])

        return template('index', scheduler=self.scheduler)


    def probes_json(self):
        probes = []
        i = 0
        for p in self.scheduler.probes:
            probes.append(self.helper_get_probe_struct(p))
            i = i + 1

        ret = {"status": "OK",
                "body": {
                    "probes": probes
                }
              }
        return json.dumps(ret)


    def helper_get_probe_data(self, probe):
        ret = []
        records = 1
        for r in self.storage.get_records_by_probe_id(probe.id, records):
            record = {
                "metadata": {
                    "probe_id": r[0],
                    "timestamp": r[2],
                    "length": r[3],
                },
                "data": str(r[4]).encode('utf-8')
            }
            if (record["data"].startswith('{') or record["data"].startswith('[')):
                try:
                    record["data"] = json.loads(record["data"])
                    if type(record["data"]) == dict:
                        record["data"] = [record["data"]]
                except:
                    pass

            ret.append(record)

        print ret
        return ret


    def helper_get_probe_filters(self, filters):
        ret = []
        for f in filters:
            ret.append(f.id)
        return ret


    def helper_get_probe_struct(self, probe):
        ret = {
            "id": "probe%s" % probe.index,
            "index": probe.index,
            "label": probe.id,
            "status": "OFF",
            "data": self.helper_get_probe_data(probe),
            "filters": self.helper_get_probe_filters(probe.filters),
            "error_filters": self.helper_get_probe_filters(probe.error_filters),
            "interval": probe.interval,
            "duration": probe.duration,
            "last_error": probe.last_error
        }
        if probe.running:
            ret["status"] = "ON"

        return ret


    def probe_json(self, p):
        ret = {"status": "OK",
                "body": self.helper_get_probe_struct(self.scheduler.probes[p])
              }
        return json.dumps(ret)


    def probe_control_json(self, p):
        command = request.forms.command
        if command == 'ON':
            self.scheduler.start_probe(p)
        elif command == 'OFF':
            self.scheduler.stop_probe(p)

        return self.probe_json(p)


    def master_json(self):
        ret = {"status": "OK",
                "body": {
                    "status": "OFF",
                    "ip_address": self.ip_address,
                    "host": self.host,
                    "uptime_secs": self.helper_get_uptime_secs(),
                    "data_size_mb": self.helper_get_data_size_mb(),
                    "free_space_mb": self.helper_get_free_space()
                }
              }
        if self.scheduler.active:
            ret["body"]["status"] = "ON"

        return json.dumps(ret)

    
    def master_control_json(self):
        command = request.forms.command
        if command == 'ON':
            self.scheduler.start_probes()
        elif command == 'OFF':
            self.scheduler.stop_probes()

        return self.master_json()


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
        return json.dumps(ret)  


    def static(self, filepath):
        return static_file(filepath, root=STATIC_ROOT)


    def helper_get_free_space(self):
        # TODO: should this be the where the data file is, not just '/'?
        stat = os.statvfs('/')
        return stat.f_bsize * stat.f_bavail


    def helper_get_uptime_secs(self):
        with open('/proc/uptime', 'r') as f:
            secs = float(f.readline().split()[0])

        return secs


    def helper_get_data_size_mb(self):
        bytes = os.path.getsize(self.config['datafile'])
        return bytes / 1024


