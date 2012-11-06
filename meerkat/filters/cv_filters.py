# -*- coding: utf-8 -*-
#
# meerkat.meerkat.filters.cv_filters
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
            filename, ext = os.path.splitext(file)
            latest_path = os.path.join(dir, "latest%s" % ext)

            os.unlink(latest_path)
            os.symlink(struct["image_path"], latest_path)

        return data


def test():
    data1 = '{ "status":"OK", "id":"meerkat.probe.camera_photo", "image_path":"/home/pi/WORKING/isoveli/meerkat/meerkat/http/static/img/test.jpg", "image_wdith":1280, "image_height":720}'

    filter = CreateLatestLink('meerkat.filters.cv_filters.CreateLatestLink')

    print(filter.filter(data1))
    assert filter.filter(data1) == data1


if __name__ == '__main__':
    test()
