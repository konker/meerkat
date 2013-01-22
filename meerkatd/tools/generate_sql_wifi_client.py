#!/usr/bin/env python
#
# generate_sql_wifi_client.py
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
# generate sql to populate wifi_client table
#

import sys
import re
import json
from storage.sqlite import Storage
import util

FIX_RE = re.compile('}{')

DDL = """CREATE TABLE IF NOT EXISTS wifi_client(
            timestamp REAL,
            utc_datetime VARCHAR,
            utc_time VARCHAR,
            mac_addr VARCHAR,
            device_id VARCHAR,
            location_id VARCHAR,
            trial_id VARCHAR,
            latitude REAL NULL,
            longitude REAL NULL);"""

ROW_SQL = "INSERT INTO wifi_client(timestamp, utc_datetime, utc_time, mac_addr, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', '%s', '%s', '%s', '%s', %f, %f);"

ROW_SQL_NO_LOC = "INSERT INTO wifi_client(timestamp, utc_datetime, utc_time, mac_addr, device_id, location_id, trial_id, latitude, longitude) VALUES(%f, '%s', '%s', '%s', '%s', '%s', '%s', NULL, NULL);"


def main():
    print DDL

    storage = Storage(sys.argv[1])
    for r in storage.get_records_by_probe_id('meerkat.probe.wifi_client_scan'):
        data = str(r[4]).encode('utf-8')
        data = FIX_RE.sub('},{', data)

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
                    print ROW_SQL_NO_LOC % (r[2], util.ts2dates(r[2]), util.ts2times(r[2]), d['MAC_Address'], r[5], r[6], r[7])
            else:
                for d in data:
                    print ROW_SQL % (r[2], util.ts2dates(r[2]), util.ts2times(r[2]), d['MAC_Address'], r[5], r[6], r[7], r[8], r[9])


if __name__ == '__main__':
    main()

