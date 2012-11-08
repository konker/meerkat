# -*- coding: utf-8 -*-
#
# util.photo_capture
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import os
import sys
import logging
from time import strftime
import json
try:
    import cv
except ImportError:
    print "Could not import cv"

DEFAULT_IMAGE_WIDTH = 1280
DEFAULT_IMAGE_HEIGHT = 720
DEFAULT_FORMAT = 'jpg'


class PhotoCapture(object):
    def __init__(self, imagepath):
        self.imagepath = imagepath


    def capture(self, filename='latest', format=DEFAULT_FORMAT, width=DEFAULT_IMAGE_WIDTH, height=DEFAULT_IMAGE_HEIGHT):

        filename = "%s.%s" % (filename, format)
        filename = os.path.realpath(os.path.join(self.imagepath, filename))

        capture = cv.CaptureFromCAM(-1)
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, width);
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height);

        img = cv.QueryFrame(capture)
        if not img:
            raise ValueError("Nothing captured")

        cv.SaveImage(filename, img)
        ret = {
            "status": "OK",
            "image_path": filename,
            "image_wdith": width,
            "image_height": height
        }
        return ret


if __name__ == '__main__':
    main()

    
