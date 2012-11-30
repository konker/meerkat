# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.cv_filters
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import logging
from meerkat.filters import BaseFilter



class Null(BaseFilter):
    def filter(self, data):
        print __name__
        return ''


def test():
    data = 'foo bar baz'
    filter = Null('meerkat.filters.util.Null')
    assert filter.filter(data1) == ''


if __name__ == '__main__':
    test()
