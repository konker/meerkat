# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

class BaseFilter(object):
    def filter(self, data):
        raise NotImplementedError()
