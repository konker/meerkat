#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.dummt_error
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys


def main():
    raise ValueError("DUMMY ERROR\nthrown to test error handling!")


if __name__ == '__main__':
    main()
