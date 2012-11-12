# -*- coding: utf-8 -*-
#
# meerkat.processes.process
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import logging
from subprocess import Popen, PIPE

class ProcessException(Exception): pass


class Process(object):
    def __init__(self, process_conf):
        self.command = process_conf
        self.process = None
        self.pid = None
        self.running = False


    # Take given data, execute command as subprocess,
    # send data to stdin, read stdout, return result to caller
    def run(self, data):
        self.process = Popen(self.command, bufsize=0, shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        self.pid = self.process.pid
        self.running = True

        stdout, stderr = self.process.communicate(data)
        if stderr:
            self.running = False
            raise ProcessException(stderr)
        else:
            self.running = False
            return stdout


    def stop(self):
        logging.debug("[%s] kill process: SIGKILL %s" % (self, self.pid))

        try:
            if self.process:
                self.process.kill()
        except OSError as ex:
            logging.error("Could not kill process: %s: %s" % (self, self.pid))


    def __str__(self):
        return "<Process: %s>" % self.command

