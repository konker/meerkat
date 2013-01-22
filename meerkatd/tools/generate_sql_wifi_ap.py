#!/usr/bin/env python
#
# generate_sql_wifi_ap.py
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
# generate sql to populate wifi_ap table
#

import sys
import re
import json
from storage.sqlite import Storage
import util


DDL = """CREATE TABLE IF NOT EXISTS wifi_ap(
            timestamp REAL,
            utc_datetime VARCHAR,
            utc_time VARCHAR,
            quality VARCHAR,
            signal_level INT,
            essid VARCHAR,
            mac_addr VARCHAR,
            channel INT,
            device_id VARCHAR,
            location_id VARCHAR,
            trial_id VARCHAR,
            latitude REAL NULL,
            longitude REAL NULL);"""

ROW_SQL = "INSERT INTO wifi_ap(timestamp, utc_datetime, utc_time, quality, signal_level, essid, mac_addr, channel, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', '%s', %d, '%s', '%s', %d, '%s', '%s', '%s', %f, %f);"

ROW_SQL_NO_LOC = "INSERT INTO wifi_ap(timestamp, utc_datetime, utc_time, quality, signal_level, essid, mac_addr, channel, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', '%s', %d, '%s', '%s', %d, '%s', '%s', '%s', NULL, NULL);"


def main():
    print DDL

    storage = Storage(sys.argv[1])
    for r in storage.get_records_by_probe_id('meerkat.probe.wifi_ap_scan'):
        data = str(r[4]).encode('utf-8')

        try:
            data = json.loads(data)
        except ValueError as ex:
            sys.stderr.write(data)
            sys.stderr.write("\n")
            sys.stderr.write("Error in JSON: %s\n" % ex)
            exit(1)

        if data:
            if r[8] == None or r[9] == None:
                for d in data:
                    try:
                        print ROW_SQL_NO_LOC % (r[2], util.ts2dates(r[2]), util.ts2times(r[2]), d['Quality'], util.dBm2i(d['Signal level']), util.esc(d['ESSID']), d['Address'], int(d['Channel']), r[5], r[6], r[7])
                    except Exception as ex:
                        sys.stderr.write("Error in DATA: %s\n" % ex)
            else:
                for d in data:
                    try:
                        print ROW_SQL % (r[2], util.ts2dates(r[2]), util.ts2times(r[2]), d['Quality'], util.dBm2i(d['Signal level']), util.esc(d['ESSID']), d['Address'], int(d['Channel']), r[5], r[6], r[7], r[8], r[9])
                    except Exception as ex:
                        sys.stderr.write("Error in DATA: %s\n" % ex)
                    


if __name__ == '__main__':
    main()

