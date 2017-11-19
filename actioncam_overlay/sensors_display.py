#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division, print_function

'''
Created on Jul 6, 2014

@author: paulg
'''

import PIL
import PIL.ImageFont
import PIL.ImageDraw
import sys

sys.path.append("../")
import dashcamData

import sys


class ArrayValueDisplay(object):
    def __init__(self, value_array, size=None, symbol_before="", symbol_after=""):
        size = [200, 60] if size is None else size
        self.array = value_array
        self.size = size
        self.symbolBefore = symbol_before
        self.symbolAfter = symbol_after
        self.init_canvas()

    def init_canvas(self):
        self.emptyCanvas = PIL.Image.new('RGBA', (self.size[0] * 3, self.size[1] * 3), (255, 255, 255, 128))
        if hasattr(self, "caption"):
            draw = PIL.ImageDraw.Draw(self.emptyCanvas)
            captionFont = PIL.ImageFont.truetype("Arial_Black.ttf", int(45))
            draw.text((0, -5), self.caption, (0, 0, 0, 255), font=captionFont)
        self.smallCanvas = self.emptyCanvas.resize(self.size, PIL.Image.ANTIALIAS)

    def draw(self, frame, fast=False):
        if frame < 0:
            frame = 0
        if frame >= len(self.array):
            frame = len(self.array) - 1
        if not fast:
            return self.draw_value(self.array[frame])
        elif fast:
            return self.draw_value_fast(self.array[frame])

    def draw_value_fast(self, value):
        temp = self.smallCanvas.copy()
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Arial.ttf", 50)
        if hasattr(self, "caption"):
            draw.text((0, 8), "%s%d%s" % (self.symbolBefore, value, self.symbolAfter), (0, 0, 0, 255), font=font)
        else:
            draw.text((5, 0), "%s%d%s" % (self.symbolBefore, value, self.symbolAfter), (0, 0, 0, 255), font=font)
        return temp

    def draw_value(self, value):
        temp = self.emptyCanvas.copy()
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Arial.ttf", 150)
        if hasattr(self, "caption"):
            draw.text((0, 25), "%s%d%s" % (self.symbolBefore, value, self.symbolAfter), (0, 0, 0, 255), font=font)
        else:
            draw.text((15, 0), "%s%d%s" % (self.symbolBefore, value, self.symbolAfter), (0, 0, 0, 255), font=font)

        img_resized = temp.resize(self.size, PIL.Image.ANTIALIAS)
        return img_resized


class HeartRateDisplay(ArrayValueDisplay):
    def __init__(self, speedF, size=[200, 60]):
        self.caption = "HEART RATE"
        super(HeartRateDisplay, self).__init__(speedF, size, symbol_before=u" heartrate ", symbol_after="")


class SensorVelocityDisplay(ArrayValueDisplay):
    def __init__(self, speedF, size=[200, 60]):
        self.caption = "SPEED"
        super(SensorVelocityDisplay, self).__init__(speedF * 60 * 2.136 / 1000., size, symbol_before=u"",
                                                    symbol_after=" km/h")


class CadenceDisplay(ArrayValueDisplay):
    def __init__(self, speedF, size=[200, 60]):
        self.caption = "CADENCE"
        super(CadenceDisplay, self).__init__(speedF, size, symbol_before="", symbol_after="/min")


class TemperatureDisplay(ArrayValueDisplay):
    def __init__(self, speedF, size=[200, 60]):
        self.caption = "TEMPERATURE"
        super(TemperatureDisplay, self).__init__(speedF, size, symbol_before=u"", symbol_after=u"deg")
