#!/usr/bin/env python
#
# catdata
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import csv
from storage.sqlite import Storage

from config.config import config

def main():
    storage = Storage(config['datafile'])
    for r in storage.get_records_by_probe_id('meerkat.probe.camera_photo', 3):
        data = str(r[4]).encode('utf-8')
        print r[0], r[1], r[2], r[3], data


if __name__ == '__main__':
    main()
