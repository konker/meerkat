#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.heartbeat
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import requests
import json

def main():
    if len(sys.argv) < 2:
        ret = { "status": "ERROR", "body": "ERROR: No url specified"}
        sys.stdout.write(json.dumps(ret))
        sys.exit(1)

    url = sys.argv[1];
    try:
        r = requests.get(url, verify=False)
        sys.stdout.write(r.text)
        sys.exit(0)
    except Exception as ex:
        ret = { "status": "ERROR", "body": str(ex) }
        sys.stdout.write(json.dumps(ret))
        sys.exit(2)


if __name__ == '__main__':
    main()

