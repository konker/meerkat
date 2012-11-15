#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.camera_photo
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import sys
from time import strftime
import json
import cv

DEFAULT_IMAGE_WIDTH = 1280
DEFAULT_IMAGE_HEIGHT = 720
DEFAULT_FORMAT = 'jpg'

def main():
    id = sys.argv[1] if len(sys.argv) > 1 else "camera_photo"
    width = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_IMAGE_WIDTH
    height = sys.argv[3] if len(sys.argv) > 2 else DEFAULT_IMAGE_HEIGHT
    format = sys.argv[4] if len(sys.argv) > 3 else DEFAULT_FORMAT

    filename = "%s-%s.%s" % (id, strftime("%Y-%m-%d_%H:%M:%S"), format)
    filename = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', '..', 'http', 'static', 'img', filename))

    try:
        capture = cv.CaptureFromCAM(-1)
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, width);
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height);

        img = cv.QueryFrame(capture)
        if not img:
            raise ValueError("Nothing captured")

        cv.SaveImage(filename, img)
        ret = {
            "status": "OK",
            "id": id,
            "image_path": filename,
            "image_width": width,
            "image_height": height
        }
        sys.stdout.write(json.dumps(ret))
    except Exception as ex:
        ret = { "status": "ERROR", "trace": str(ex) }
        sys.stderr.write(json.dumps(ret))


if __name__ == '__main__':
    main()

