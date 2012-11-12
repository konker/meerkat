#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probe.camera_photo
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

        storage = cv.CreateMemStorage(0)
        detected = list(cv.HOGDetectMultiScale(img, storage, win_stride=(8,8),
                        padding=(32,32), scale=1.05, group_threshold=2))

        detected = filter_detected(detected)
        draw_detected(img, detected)

        cv.SaveImage(filename, img)
        ret = {
            "status": "OK",
            "id": id,
            "image_path": filename,
            "image_width": width,
            "image_height": height,
            "detected": detected
        }
        sys.stdout.write(json.dumps(ret))
    except Exception as ex:
        ret = { "status": "ERROR", "trace": str(ex) }
        sys.stderr.write(json.dumps(ret))


def filter_detected(detected):
    def inside(r, q):
        (rx, ry), (rw, rh) = r
        (qx, qy), (qw, qh) = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

    filtered = []
    for r in detected:
        insidef = False
        for q in detected:
            if inside(r, q):
                insidef = True
                break
        if not insidef:
            filtered.append(r)

    return filtered


def draw_detected(img, detected, thickness = 1):
    for r in detected:
        (rx, ry), (rw, rh) = r
        tl = (rx + int(rw*0.1), ry + int(rh*0.07))
        br = (rx + int(rw*0.9), ry + int(rh*0.87))
        cv.Rectangle(img, tl, br, (0, 255, 0), 3)
    return 


if __name__ == '__main__':
    main()


