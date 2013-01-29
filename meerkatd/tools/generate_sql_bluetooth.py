#!/usr/bin/env python
#
# generate_sql_bluetooth.py
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
# generate sql to populate bluetooth table
#

import sys
import re
import json
from storage.sqlite import Storage                                            
import util

DDL = """CREATE TABLE IF NOT EXISTS bluetooth(
            timestamp REAL,
            utc_datetime VARCHAR,
            utc_time VARCHAR,
            bluetooth_device_class INT,
            bluetooth_name VARCHAR,
            bluetooth_addr VARCHAR,
            device_id VARCHAR,
            location_id VARCHAR,
            trial_id VARCHAR,
            latitude REAL NULL,
            longitude REAL NULL);"""

ROW_SQL = "INSERT INTO bluetooth(timestamp, utc_datetime, utc_time, bluetooth_device_class, bluetooth_name, bluetooth_addr, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s', %f, %f);"

ROW_SQL_NO_LOC = "INSERT INTO bluetooth(timestamp, utc_datetime, utc_time, bluetooth_device_class, bluetooth_name, bluetooth_addr, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s', NULL, NULL);"


def main():
    print DDL

    storage = Storage(sys.argv[1])
    for r in storage.get_records_by_probe_id('meerkat.probe.bluetooth'):
        data = str(r[3]).encode('utf-8')

        try:
            data = json.loads(data)
        except ValueError as ex:
            sys.stderr.write(data)
            sys.stderr.write("\n")
            sys.stderr.write("Error in JSON: %s\n" % ex)
            exit(1)

        if data:
            if r[7] == None or r[8] == None:
                for d in data:
                    try:
                        print ROW_SQL_NO_LOC % (r[1], util.ts2dates(r[1]), util.ts2times(r[1]), d.get('DEVICE_CLASS', ''), util.esc(d.get('NAME')), d.get('ADDRESS', ''), r[4], r[5], r[6])
                    except Exception as ex:
                        try:
                            print ROW_SQL_NO_LOC % (r[1], util.ts2dates(r[1]), util.ts2times(r[1]), d['device_class'], d['name'], d['address'], r[5], r[6], r[7])
                        except Exception as ex:
                            sys.stderr.write("%f" % r[1])
                            sys.stderr.write("\n")
                            sys.stderr.write("Error in DATA: %s\n" % ex)
            else:
                for d in data:
                    try:
                        print ROW_SQL % (r[1], util.ts2dates(r[1]), util.ts2times(r[1]), d.get('DEVICE_CLASS', ''), util.esc(d.get('NAME', '')), d.get('ADDRESS', ''), r[4], r[5], r[6], r[7], r[8])
                    except Exception as ex:
                        try:
                            print ROW_SQL % (r[1], util.ts2dates(r[1]), util.ts2times(r[1]), d.get('device_class', ''), d.get('name', ''), d.get('address', ''), r[4], r[5], r[6], r[7], r[8])
                        except Exception as ex:
                            sys.stderr.write("%f" % r[1])
                            sys.stderr.write("\n")
                            sys.stderr.write("Error in DATA: %s\n" % ex)


if __name__ == '__main__':
    main()

