# -*- coding: utf-8 -*-
#
# meerkat.scheduler.data_cache
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import sys
import time
import logging

class DataCache(object):
    def __init__(self):
        self.cache = {}
        self.timestamps = {}


    def put(self, id, data):
        self.cache[id] = data
        self.timestamps[id] = time.time() * 1000


    def get(self, id, default=None):
        return self.cache.get(id, default)


    def get_fresh(self, id, max_age_ms, default=None):
        age = (time.time() * 1000) - self.timestamps.get(id, 0)
        print age
        print max_age_ms
        if age > 0 and age < max_age_ms:
            return self.cache.get(id, default)

        return default

    def delete(self, id):
        if id in self.cache:
            del self.cache[id]
            del self.timestamps[id]


