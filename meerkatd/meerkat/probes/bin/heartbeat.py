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
        print(json.dumps(ret))
        sys.exit(1)

    url = sys.argv[1];
    try:
        r = requests.get(url, verify=False)
        print(r.text)
    except Exception as ex:
        ret = { "status": "ERROR", "body": str(ex) }
        print(json.dumps(ret))
        sys.exit(2)


if __name__ == '__main__':
    main()

