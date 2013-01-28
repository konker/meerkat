# -*- coding: utf-8 -*-
#
# meerkat.http.http
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import traceback
import time
from datetime import datetime
import logging
import re
from threading import Thread
from subprocess import check_output, Popen, PIPE
import json
import socket
import requests
import bottle
from bottle import template, static_file, request, response, redirect
from storage.sqlite import Storage
from util.photo_capture import PhotoCapture
#from meerkat.scheduler import COMMAND_EXEC

THREE_MINS_MS = 1000 * 60 * 3

bottle.TEMPLATE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'views')),
STATIC_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


class HttpServer(object):
    def __init__(self, scheduler, config):
        self.scheduler = scheduler
        self.config = config
        self.photo_capture = PhotoCapture(config["imagepath"])

        self.host = socket.gethostname()
        self.short_host = self.helper_get_short_host()
        self.ip_address = socket.gethostbyname(self.host)
        self.ip_address2 = self.helper_get_ip_address2()

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
        bottle.route('/meerkat/data', method='GET')(self.data_tgz)
        bottle.route('/meerkat/kickstart_gps.json', method='POST')(self.kickstart_gps_control_json)
        bottle.route('/meerkat/gps_procs.json', method='GET')(self.gps_procs_json)
        bottle.route('/meerkat/join_click_wifi.json', method='GET')(self.join_click_wifi)
        bottle.route('/meerkat/join_city_wifi.json', method='GET')(self.join_city_wifi)
        bottle.route('/meerkat/cleanup_gps.json', method='POST')(self.cleanup_gps_control_json)


    def start(self):
        self.http_thread = Thread(target=bottle.run,
                                  kwargs=dict(host=self.config['http_host'],
                                              port=self.config['http_port'],
                                              server='cherrypy',
                                              debug=False,
                                              quiet=True),
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
        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def probe_json(self, p):
        ret = {"status": "OK",
                "body": self.helper_get_probe_struct(self.scheduler.probes[p])
              }
        response.set_header("Cache-Control", "No-store")
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
        response.set_header("Cache-Control", "No-store")
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

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def master_json(self):
        ret = {"status": "OK",
                "body": self.helper_get_master_struct()
        }

        response.set_header("Cache-Control", "No-store")
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
        response.set_header("Cache-Control", "No-store")
        return self.master_json()

    
    def register_control_json(self):
        try:
            r = requests.post(self.config["mission_control"]["register_url"], data=self.info_json())
            ret = r.text
        except Exception as ex:
            ret = json.dumps({"status": "ERROR", "body": traceback.format_exc() })

        response.set_header("Cache-Control", "No-store")
        return ret

    
    def capture_control_json(self):
        ret = {"status": "OK",
                "body": "Camera image captured"
              }
        try:
            ret["body"] = self.photo_capture.capture()
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
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

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)  


    def data_tgz(self):
        cmd = "tar -czf - -C %s . -C %s ." % (os.path.dirname(self.config["datafile"]), self.config["imagepath"])
        filename = "%s-data-%s.tgz" % (self.host, datetime.today().isoformat())

        try:
            proc = Popen(cmd.split(' '), bufsize=0, shell=False, stdout=PIPE)

            response.set_header('Content-Type', 'application/octet-stream')
            response.set_header('Content-Disposition',
                                "Attachment;filename=%s" % filename)
            for l in proc.stdout:
                yield l

        except:
            yield traceback.format_exc()


    def gps_procs_json(self):
        ret = {"status": "OK",
               "body": "GPS procs: ?"}

        cmd = os.path.join(self.config["binpath"], 'gps_procs.sh')
        try:
            ret["body"] = check_output(cmd, shell=True)
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def join_click_wifi(self):
        ret = {"status": "OK",
               "body": "GPS procs: ?"}

        cmd = os.path.join(self.config["binpath"], 'join_click_wifi.sh')
        try:
            ret["body"] = check_output(cmd, shell=True)
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def join_city_wifi(self):
        ret = {"status": "OK",
               "body": "GPS procs: ?"}

        cmd = os.path.join(self.config["binpath"], 'join_city_wifi.sh')
        try:
            ret["body"] = check_output(cmd, shell=True)
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def cleanup_gps_control_json(self):
        ret = {"status": "OK",
               "body": "GPS processes cleaned up"}

        cmd = os.path.join(self.config["binpath"], 'cleanup_gps.sh')
        try:
            ret["body"] = check_output(cmd, shell=True)
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def kickstart_gps_control_json(self):
        ret = {"status": "OK",
               "body": "GPS Kickstarted"}

        cmd = os.path.join(self.config["binpath"], 'kickstart_gps.sh')
        try:
            output = check_output(cmd, shell=True)
        except:
            ret["status"] = "ERROR"
            ret["body"] = traceback.format_exc()

        response.set_header("Cache-Control", "No-store")
        return json.dumps(ret)


    def static(self, filepath):
        if 'latest' in filepath:
            response.set_header("Cache-Control", "No-store")

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
                    "timestamp": r[1],
                    "length": r[2],
                },
                "data": str(r[3]).encode('utf-8')
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
            "all_on": self.scheduler.all_probes_on(),
            "all_off": self.scheduler.all_probes_off(),
            "ip_address": self.ip_address,
            "ip_address2": self.ip_address2,
            "net_interfaces": self.helper_get_net_interfaces(),
            "cur_essid": self.helper_get_cur_essid(),
            "host": self.host,
            "short_host": self.short_host,
            "heartbeat_url": "https://%s/meerkat/heartbeat.json" % (self.host),
            "info_url": "https://%s/meerkat/info.json" % (self.host),
            "dashboard_url": "https://%s/meerkat/" % (self.host),
            "dashboard_url_short_host": "https://%s/meerkat/" % (self.short_host),
            "dashboard_url_ip_address": "https://%s/meerkat/" % (self.ip_address),
            "dashboard_url_ip_address2": "https://%s/meerkat/" % (self.ip_address2),
            "latest_img_url": "https://%s/static/img/latest.jpg?%s" % (self.host, time.time()),
            "uptime_secs": self.helper_get_uptime_secs(),
            "load_average": self.helper_get_load_average(),
            "sys_temperature": self.helper_get_sys_temperature(),
            "gpu_temperature": self.helper_get_gpu_temperature(),
            "data_size_kb": self.helper_get_data_size_kb(),
            "image_data_size_kb": self.helper_get_image_data_size_kb(),
            "free_space_b": self.helper_get_free_space(),
            "has_camera": self.config["has_camera"],
            "location": self.helper_get_location(),
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


    def helper_get_location(self):
        location = {"latitude": '?', "longitude": '?'}

        cached_location = self.scheduler.cache.get_fresh("meerkat.probe.gps_info", THREE_MINS_MS)
        if cached_location:
            cached_location = cached_location[0]
            if 'latitude' in cached_location and 'longitude' in cached_location:

                location["latitude"] = cached_location['latitude']
                location["longitude"] = cached_location['longitude']

        return location


    def helper_get_free_space(self):
        # TODO: should this be the where the data file is, not just '/'?
        stat = os.statvfs('/')
        return stat.f_bsize * stat.f_bavail


    def helper_get_ip_address2(self):
        ip_address2 = '?'
        cmd = 'hostname -I'
        try:
            ip_address2 = check_output(cmd, shell=True).strip()
        except:
            pass

        return ip_address2


    def helper_get_cur_essid(self):
        cur_essid = '?'
        cmd = 'sudo wpa_cli list_networks | grep CURRENT | cut -f 2'
        try:
            cur_essid = check_output(cmd, shell=True)
            if cur_essid == '':
                cur_essid = '?'
        except:
            pass

        return cur_essid


    def helper_get_short_host(self):
        short_host = '?'
        cmd = 'hostname -s'
        try:
            short_host = check_output(cmd, shell=True).strip()
        except:
            pass

        return short_host


    def helper_get_net_interfaces(self):
        net_interfaces = '?'
        cmd = 'ifconfig -s -a | sed 1d | cut -d " " -f1 | tr "\\\\n" ,'
        try:
            net_interfaces = check_output(cmd, shell=True).split(',')
            net_interfaces.pop()
            net_interfaces.pop()
        except:
            pass

        return net_interfaces


    def helper_get_uptime_secs(self):
        uptime = '?'
        try:
            with open('/proc/uptime', 'r') as f:
                secs = f.readline()

            uptime = float(secs.split()[0])
        except:
            pass

        return uptime


    def helper_get_gpu_temperature(self):
        gpu_temperature = '?'
        cmd = '/opt/vc/bin/vcgencmd measure_temp | egrep "[0-9.]*" -o'
        try:
            gpu_temperature = check_output(cmd, shell=True)
        except:
            pass

        return float(gpu_temperature)


    def helper_get_sys_temperature(self):
        sys_temperature = '?'
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                sys_temperature = f.readline()

            sys_temperature = float(sys_temperature) / 1000
        except:
            pass

        return sys_temperature


    def helper_get_load_average(self):
        load_average = '?'
        try:
            with open('/proc/loadavg', 'r') as f:
                loadavg = f.readline()

            loadavg = loadavg.split(' ')
            loadavg = loadavg[:-2]
        except:
            pass

        return loadavg


    def helper_get_memory_info(self):
        meminfo = ('?', '?')
        try:
            with open('/proc/meminfo', 'r') as f:
                available_mem = f.readline()
                free_mem = f.readline()

            meminfo = (int(available_mem.split()[1]), int(free_mem.split()[1]))
        except:
            pass

        return meminfo


    def helper_get_data_size_kb(self):
        bytes = os.path.getsize(self.config['datafile'])
        return bytes / 1024


    def helper_get_image_data_size_kb(self):
        bytes = 0
        for root, dirs, files in os.walk(self.config['imagepath']):
            bytes = sum(os.path.getsize(os.path.join(root, image)) for image in files)
        return bytes / 1024


