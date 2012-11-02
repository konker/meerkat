# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.uppercase
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

from meerkat.filters import BaseFilter


class RemoveErrors(BaseFilter):
    def filter(self, data):
        for l in data.split("\n"):
            if l.startswith('VIDIOC_QUERYMENU'):
                continue
            else:
                return l

