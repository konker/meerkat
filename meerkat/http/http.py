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
from storage.sqlite import Storage
from util.photo_capture import PhotoCapture
from meerkat.scheduler import COMMAND_EXEC

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


class HttpServer(object):
    def __init__(self, scheduler, config):
        self.scheduler = scheduler
        self.config = config
        self.storage = None
        self.photo_capture = PhotoCapture(config["imagepath"])

        self.host = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host)

        # set up the routes manually
        bottle.route('/static/<filepath:path>', method='GET')(self.static)
        bottle.route('/', method='GET')(self.index)
        bottle.route('/master.json', method='GET')(self.master_json)
        bottle.route('/master.json', method='POST')(self.master_control_json)
        bottle.route('/capture.json', method='POST')(self.capture_control_json)
        bottle.route('/probes.json', method='GET')(self.probes_json)
        bottle.route('/probe<p:int>.json', method='GET')(self.probe_json)
        bottle.route('/probe<p:int>.json', method='POST')(self.probe_control_json)
        bottle.route('/log.json', method='GET')(self.log_json)


    def start(self):
        '''
        bottle.run(host=self.config['http_host'], port=self.config['http_port'], debug=False, server='wsgiref')
        '''
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host=self.config['http_host'], port=self.config['http_port'], server='wsgiref', debug=False, quiet=True),
                                  name='http-thread')
        self.http_thread.setDaemon(True)
        self.http_thread.start()
        logging.info("Http server started.")


    def index(self):
        # [FIXME: homepage must be called before storage is used]
        if not self.storage:
            self.storage = Storage(self.config["datafile"])
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
        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)


    def probe_json(self, p):
        ret = {"status": "OK",
                "body": self.helper_get_probe_struct(self.scheduler.probes[p])
              }
        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)


    def probe_control_json(self, p):
        command = request.forms.command
        if command == 'ON':
            #self.scheduler.start_probe(p)
            self.scheduler.queue.put( (COMMAND_EXEC, 'start_probe', p) )
        elif command == 'OFF':
            #self.scheduler.stop_probe(p)
            self.scheduler.queue.put( (COMMAND_EXEC, 'stop_probe', p) )

        time.sleep(0.5)
        response.set_header('Cache-Control', 'No-store')
        return self.probe_json(p)


    def master_json(self):
        ret = {"status": "OK",
                "body": {
                    "status": "OFF",
                    "ip_address": self.ip_address,
                    "host": self.host,
                    "uptime_secs": self.helper_get_uptime_secs(),
                    "data_size_mb": self.helper_get_data_size_mb(),
                    "free_space_mb": self.helper_get_free_space(),
                    "has_camera": self.config["has_camera"],
                    "available_memory_kb": 0,
                    "free_memory_kb": 0
                }
        }

        if self.scheduler.active:
            ret["body"]["status"] = "ON"

        available_mem, free_mem = self.helper_get_memory_info()
        ret["body"]["available_memory_kb"] = available_mem
        ret["body"]["free_memory_kb"] = free_mem

        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)

    
    def master_control_json(self):
        command = request.forms.command
        if command == 'ON':
            #self.scheduler.start_probes()
            self.scheduler.queue.put( (COMMAND_EXEC, 'start_probes') )
        elif command == 'OFF':
            #self.scheduler.stop_probes()
            self.scheduler.queue.put( (COMMAND_EXEC, 'stop_probes') )

        time.sleep(1)
        response.set_header('Cache-Control', 'No-store')
        return self.master_json()

    
    def capture_control_json(self):
        ret = {"status": "OK",
                "body": None
              }
        try:
            ret["body"] = self.photo_capture.capture()
        except Exception as ex:
            ret["status"] = "ERROR"
            ret["body"] = str(ex)

        response.set_header('Cache-Control', 'No-store')
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


    def static(self, filepath):
        if 'latest' in filepath:
            response.set_header('Cache-Control', 'No-store')

        return static_file(filepath, root=STATIC_ROOT)


    ######### HELPERS ########################################################
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
            "command": ' '.join(probe.command),
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


    def helper_get_free_space(self):
        # TODO: should this be the where the data file is, not just '/'?
        stat = os.statvfs('/')
        return stat.f_bsize * stat.f_bavail


    def helper_get_uptime_secs(self):
        with open('/proc/uptime', 'r') as f:
            secs = f.readline()

        return float(secs.split()[0])


    def helper_get_memory_info(self):
        with open('/proc/meminfo', 'r') as f:
            available_mem = f.readline()
            free_mem = f.readline()

        return (int(available_mem.split()[1]), int(free_mem.split()[1]))


    def helper_get_data_size_mb(self):
        bytes = os.path.getsize(self.config['datafile'])
        return bytes / 1024


