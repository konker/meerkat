# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

class BaseFilter(object):
    def __init__(self, id):
        self.id = id


    def filter(self, data):
        raise NotImplementedError()
