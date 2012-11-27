#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# get_location
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import gps
import json


def handle_packet(p):
    if p['class'] == 'TPV':
        return p

    return p


def main():
    session = gps.gps(mode=gps.WATCH_ENABLE)

    while True:
        packet = handle_packet(session.next())
        if packet:
            print packet

    session.close()


if __name__ == '__main__':
    main()
