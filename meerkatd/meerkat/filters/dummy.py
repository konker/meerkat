# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.uppercase
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

from meerkat.filters import BaseFilter


class Uppercase(BaseFilter):
    def filter(self, data):
        return str(data).upper()


class Lowercase(BaseFilter):
    def filter(self, data):
        return str(data).lower()

