#!/usr/bin/env python
#
# generate_csv.py
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
# generate csv from given database and table
#

import sys
from storage.sqlite import Storage                                            
import csv
import util


def main():
    storage = Storage(sys.argv[1])
    fields = storage.get_fields(sys.argv[2])
    writer = csv.writer(sys.stdout)

    writer.writerow(fields)
    for r in storage.get_records_by_table(sys.argv[2]):
        writer.writerow(r)


if __name__ == '__main__':
    main()


