# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.uppercase
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import logging
import json
from meerkat.filters import BaseFilter


class RemoveErrors(BaseFilter):
    def filter(self, data):
        for l in data.split("\n"):
            if l.startswith('VIDIOC_QUERYMENU'):
                continue
            else:
                return l


class CreateLatestLink(BaseFilter):
    def filter(self, data):
        struct = json.loads(data)
        if struct["status"] == "OK":
            dir, file = os.path.split(struct["image_path"])
            filename, ext = file.split('.')
            latest_path = os.path.join(dir, "latest.%s" % ext)

            print struct["image_path"] 
            print latest_path
            os.symlink(struct["image_path"], latest_path)

        return data

def test():
    data = '{ "status":"OK", "id":"meerkat.probe.camera_photo", "image_path":"/home/pi/WORKING/isoveli/meerkat/meerkat/http/static/images/test.jpg", "image_wdith":1280, "image_height":720}'
    filter = CreateLatestLink()
    print(filter.filter(data))
    assert filter.filter(data) == data


if __name__ == '__main__':
    test()
