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
import logging
import json
import cv

def main(input):
    struct = json.loads(input)
    logging.info("PROC INPUT:")
    logging.info(input)
    logging.info("PROC STRUCT:")
    logging.info(struct)

    try:
        storage = cv.CreateMemStorage(0)
        img = cv.LoadImage(struct["image_path"])

        detected = list(cv.HOGDetectMultiScale(img, storage, win_stride=(8,8),
                        padding=(32,32), scale=1.05, group_threshold=2))

        detected = filter_detected(detected)
        struct["detected"] = detected

        sys.stdout.write(json.dumps(struct))
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


if __name__ == '__main__':
    main(sys.stdin.read())


