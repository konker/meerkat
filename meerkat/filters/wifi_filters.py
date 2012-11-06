# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.wifi_filters
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import logging
import json
from meerkat.filters import BaseFilter


class RemoveWarnings(BaseFilter):
    def filter(self, data):
        for l in data.split("\n"):
            if l.startswith('WARNING'):
                continue
            else:
                return l


