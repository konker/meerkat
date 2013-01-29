#!/usr/bin/env python
#
# filter_data.sql.py
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
# generate sql to filter data outside of the given start and end timestamps
#

import sys
import util

def main():
    start = None
    end = None

    try:
        start = util.dates2ts(sys.argv[1])
        end   = util.dates2ts(sys.argv[2])
    except:
        pass

    if start and end:
        if start < end:
            print "DELETE FROM probe_data WHERE timestamp < %s;" % start
            print "DELETE FROM probe_data WHERE timestamp > %s;" % end


if __name__ == '__main__':
    main()

