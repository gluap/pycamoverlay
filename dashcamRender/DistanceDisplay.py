'''
Created on Jul 6, 2014

@author: paulg
'''
from __future__ import print_function, absolute_import, division, unicode_literals
import PIL
import PIL.ImageFont
import PIL.ImageDraw
import sys

sys.path.append("../")
import dashcamData


class DistanceDisplay(object):
    def __init__(self, distances, size=None, fast=False):
        size = size if size is not None else [300, 60]
        self.distances = distances
        self.size = size
        if not fast:
            self.scale_bar = ScaleBar(width=size[0] * 3, height=size[1] * 3)
        else:
            self.scale_bar = ScaleBar(width=size[0], height=size[1])

    def fast_draw(self, frame):
        temp = self.scale_bar.draw(self.distances.getDistance(frame), sigma=self.distances.getSigma(frame))
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 17)
        draw.text((10, 10), "%0.1f(%0.1f)" % (self.distances.getDistance(frame), self.distances.getSigma(frame)),
                  (0, 0, 0, 255), font=font)
        return temp

    def draw(self, frame, fast=False):
        if fast:
            return self.fast_draw(frame)
        else:
            return self.slowDraw(frame)

    def slowDraw(self, frame):
        temp = self.scale_bar.draw(self.distances.getDistance(frame), sigma=self.distances.getSigma(frame))
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 50)
        draw.text((10, 10), "%0.1f(%0.1f)" % (self.distances.getDistance(frame), self.distances.getSigma(frame)),
                  (0, 0, 0, 255), font=font)
        img_resized = temp.resize(self.size, PIL.Image.ANTIALIAS)
        return img_resized


class ScaleBar(object):
    def __init__(self, min_value=0, max_value=200, bad_value=150, width=300, height=60):
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.bad_value = bad_value
        self.delta = max_value - min_value
        self.bad_width = 1. * (self.bad_value - self.min_value) / self.delta * self.width

    def draw(self, value, sigma=0.):
        temp = PIL.Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        width = 1. * (value - self.min_value) / self.delta * self.width
        width_sigma = sigma / self.delta * self.width
        draw = PIL.ImageDraw.Draw(temp)
        if value < self.bad_value:
            fColor = (255, 0, 0, 150)
        else:
            fColor = (0, 180, 0, 150)
        draw.rectangle([self.width - width, 0, self.width, self.height / 2], fill=fColor)
        draw.rectangle([0, 0, self.width - width, self.height / 2], fill=(255, 255, 255, 150))
        draw.line((self.width - width, 0, self.width - width, self.height / 2), fill=(255, 255, 255, 200),
                  width=int(width_sigma) + 1)
        draw.line((self.width - self.bad_width, 0, self.width - self.bad_width, self.height / 2 + 16),
                  fill=(0, 0, 0, 200), width=3)

        return temp
