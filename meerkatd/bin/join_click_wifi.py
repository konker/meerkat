#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# join_click_wifi
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import time
import re
import requests
from bs4 import BeautifulSoup

INIT_URL = 'http://ipv4.0-9.fi/'

def main():
    kohde = 'Kamppi'

    r = requests.get(INIT_URL)
    #soup = BeautifulSoup(r.text)
    print r.url
    src_re = re.compile('src="([^"]+)"')
    href_re = re.compile('href="([^"]+)"')
    kohde_js_str_re = re.compile("'\+kohde\+'")
    js_str_re = re.compile("'\+[^+]*\+'")
    js_date_str_re = re.compile("'\+new Date\(\).getTime\(\)\+'")

    srcs = src_re.findall(r.text)
    return
    for src in srcs:
        src = js_date_str_re.sub(str(int(time.time())), src)
        src = js_str_re.sub(kohde, src)
        src = js_str_re.sub('', src)
        if '.php' in src:
            print src
            print '---'
            rr = requests.get(src, headers={'Referer': r.url})
            hrefs = href_re.findall(rr.text)
            for href in hrefs:
                print href
                print '==='
                rrr = requests.get(href, headers={'Referer': rr.url})
                print rrr.text


if __name__ == '__main__':
    main()

