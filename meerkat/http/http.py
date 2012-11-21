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
from subprocess import check_output
import json
import socket
import requests
import bottle
from bottle import template, static_file, request, response, redirect
from storage.sqlite import Storage
from util.photo_capture import PhotoCapture
#from meerkat.scheduler import COMMAND_EXEC

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


class HttpServer(object):
    def __init__(self, scheduler, config):
        self.scheduler = scheduler
        self.config = config
        self.photo_capture = PhotoCapture(config["imagepath"])

        self.host = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host)

        # set up the routes manually
        bottle.route('/static/<filepath:path>', method='GET')(self.static)
        bottle.route('/', method='GET')(self.index)
        bottle.route('/meerkat/', method='GET')(self.meerkat)
        bottle.route('/meerkat/heartbeat.json', method='GET')(self.register_control_json)
        bottle.route('/meerkat/info.json', method='GET')(self.info_json)
        bottle.route('/meerkat/master.json', method='GET')(self.master_json)
        bottle.route('/meerkat/master.json', method='POST')(self.master_control_json)
        bottle.route('/meerkat/register.json', method='POST')(self.register_control_json)
        bottle.route('/meerkat/capture.json', method='POST')(self.capture_control_json)
        bottle.route('/meerkat/probes.json', method='GET')(self.probes_json)
        bottle.route('/meerkat/probe<p:int>.json', method='GET')(self.probe_json)
        bottle.route('/meerkat/probe<p:int>.json', method='POST')(self.probe_control_json)
        bottle.route('/meerkat/log.json', method='GET')(self.log_json)


    def start(self):
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host=self.config['http_host'], port=self.config['http_port'], server='wsgiref', debug=False, quiet=True),
                                  name='http-thread')
        self.http_thread.setDaemon(True)
        self.http_thread.start()
        logging.info("Http server started on port %s." % self.config["http_port"])


    def index(self):
        redirect('/meerkat/')


    def meerkat(self):
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
            self.scheduler.start_probe(p)
            #self.scheduler.queue.put( (COMMAND_EXEC, 'start_probe', p) )
        elif command == 'OFF':
            self.scheduler.stop_probe(p)
            #self.scheduler.queue.put( (COMMAND_EXEC, 'stop_probe', p) )

        time.sleep(0.5)
        response.set_header('Cache-Control', 'No-store')
        return self.probe_json(p)


    def info_json(self):
        probes = []
        i = 0
        for p in self.scheduler.probes:
            probes.append(self.helper_get_probe_struct(p))
            i = i + 1

        ret = {"status": "OK",
                "body": {
                    "id": None,
                    "info": self.helper_get_master_struct(),
                    "probes": probes
                }
              }
        ret["body"]["id"] = ret["body"]["info"]["host"]

        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)


    def master_json(self):
        ret = {"status": "OK",
                "body": self.helper_get_master_struct()
        }

        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)

    
    def master_control_json(self):
        command = request.forms.command
        if command == 'ON':
            self.scheduler.start_probes()
            #self.scheduler.queue.put( (COMMAND_EXEC, 'start_probes') )
        elif command == 'OFF':
            self.scheduler.stop_probes()
            #self.scheduler.queue.put( (COMMAND_EXEC, 'stop_probes') )

        time.sleep(1)
        response.set_header('Cache-Control', 'No-store')
        return self.master_json()

    
    def register_control_json(self):
        ret = {"status": "OK",
                "body": ""
              }
        try:
            r = requests.post(self.config["mission_control"]["register_url"], data=self.info_json())
            ret = r.text
        except Exception as ex:
            ret["status"] = "ERROR"
            ret["body"] = str(ex)

        response.set_header('Cache-Control', 'No-store')
        return json.dumps(ret)

    
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
        storage = Storage(self.config["datafile"])
        for r in storage.get_records_by_probe_id(probe.id, records):
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

        storage.close()
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
            "dummy": probe.dummy,
            "last_error": probe.last_error
        }
        if probe.running:
            ret["status"] = "ON"

        return ret


    def helper_get_master_struct(self):
        ret = {
            "timestamp": time.time() * 1000,
            "status": "OFF",
            "ip_address": self.ip_address,
            "net_interfaces": self.helper_get_net_interfaces(),
            "host": self.host,
            "heartbeat_url": "https://%s/meerkat/heartbeat.json" % (self.host),
            "info_url": "https://%s/meerkat/info.json" % (self.host),
            "dashboard_url": "https://%s/meerkat/" % (self.host),
            "latest_img_url": "https://%s/static/img/latest.jpg?%s" % (self.host, time.time()),
            "uptime_secs": self.helper_get_uptime_secs(),
            "load_average": self.helper_get_load_average(),
            "data_size_kb": self.helper_get_data_size_kb(),
            "free_space_b": self.helper_get_free_space(),
            "has_camera": self.config["has_camera"],
            "available_memory_kb": 0,
            "free_memory_kb": 0,
            "mission_control_url": self.config['mission_control']['url'],
            "mission_control_register_url": self.config['mission_control']['register_url']
        }

        if self.scheduler.active:
            ret["status"] = "ON"

        available_mem, free_mem = self.helper_get_memory_info()
        ret["available_memory_kb"] = available_mem
        ret["free_memory_kb"] = free_mem

        return ret

    def helper_get_free_space(self):
        # TODO: should this be the where the data file is, not just '/'?
        stat = os.statvfs('/')
        return stat.f_bsize * stat.f_bavail


    def helper_get_net_interfaces(self):
        net_interfaces = '?'
        cmd = 'ifconfig -s -a | sed 1d | cut -d " " -f1 | tr "\\\\n" ,'
        try:
            net_interfaces = check_output(cmd, shell=True).split(',')
            net_interfaces.pop()
            net_interfaces.pop()
        except IOError:
            pass

        return net_interfaces


    def helper_get_uptime_secs(self):
        uptime = '?'
        try:
            with open('/proc/uptime', 'r') as f:
                secs = f.readline()

            uptime = float(secs.split()[0])
        except IOError:
            pass

        return uptime


    def helper_get_load_average(self):
        load_average = '?'
        try:
            with open('/proc/loadavg', 'r') as f:
                loadavg = f.readline()

            loadavg = loadavg.split(' ')
            loadavg = loadavg[:-2]
        except IOError:
            pass

        return loadavg


    def helper_get_memory_info(self):
        meminfo = ('?', '?')
        try:
            with open('/proc/meminfo', 'r') as f:
                available_mem = f.readline()
                free_mem = f.readline()

            meminfo = (int(available_mem.split()[1]), int(free_mem.split()[1]))
        except IOError:
            pass

        return meminfo


    def helper_get_data_size_kb(self):
        bytes = os.path.getsize(self.config['datafile'])
        return bytes / 1024


