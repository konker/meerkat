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
        if data.startswith('WARNING'):
            return ''

        return data

