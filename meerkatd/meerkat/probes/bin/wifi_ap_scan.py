#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.wifi_ap_scan
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import json
from subprocess import check_output

ignore_list = ['Bit Rates']

def main():
    cmd = ['sudo', 'iwlist', 'wlan0', 'scan']
    raw = check_output(cmd, shell=False)

    info = parse_raw(raw)
    sys.stdout.write(json.dumps(info))


def parse_raw(raw):
    ret = []
    cur_cell = None
    for l in raw.split("\n"):
        l = l.strip()
        if l.startswith('Cell '):
            if cur_cell:
                ret.append(cur_cell)

            cur_cell = {}
            handle_cell_start(l, cur_cell)
        elif cur_cell:
            handle_cell_item(l, cur_cell)

    if cur_cell:
        ret.append(cur_cell)

    return ret


def handle_cell_start(l, cur_cell):
    x,l = l.split(' - ')
    handle_cell_item(l, cur_cell)


def handle_cell_item(l, cur_cell):
    if l is not None and l != '':
        if not ':' in l:
            for part in  l.split('  '):
                if '=' in part:
                    k,v = part.split('=', 1)
                    cur_cell[k] = v.translate(None, '"')
        else:
            k,v = l.split(':', 1)
            if k in ignore_list:
                return

            cur_cell[k] = v.translate(None, '"')


'''
Example raw output:

          Cell 01 - Address: A4:56:30:E8:07:E0
                    ESSID:"aalto open"
                    Protocol:IEEE 802.11bg
                    Mode:Master
                    Frequency:2.412 GHz (Channel 1)
                    Encryption key:off
                    Bit Rates:54 Mb/s
                    Quality=87/100  Signal level=60/100  
          Cell 02 - Address: A4:56:30:E8:07:E1
                    ESSID:"eduroam"
                    Protocol:IEEE 802.11bg
                    Mode:Master
                    Frequency:2.412 GHz (Channel 1)
                    Encryption key:on
                    Bit Rates:54 Mb/s
                    Extra:rsn_ie=30140100000fac040100000fac040100000fac012800
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : CCMP
                        Pairwise Ciphers (1) : CCMP
                        Authentication Suites (1) : 802.1x
                    Quality=90/100  Signal level=50/100  
'''


if __name__ == '__main__':
    main()

