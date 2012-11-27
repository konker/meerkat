#!/usr/bin/env python
#
# catdb
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import csv
from storage.sqlite import Storage

from config.config import config

"""
Print each database record in csv format to stdout
"""
def main():
    writer = csv.writer(sys.stdout)
    storage = Storage(config['datafile'])
    for r in storage.reader():
        if r[0] == 0x40:
            # camera
            fname ="%s-%s.jpg" % (r[0], r[1]) 
            with open(fname, 'w') as f:
                f.write(r[3])
            print "wrote: %s" % fname
        else:
            writer.writerow(r)


if __name__ == '__main__':
    main()
