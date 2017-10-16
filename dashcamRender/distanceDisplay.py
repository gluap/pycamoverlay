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


class distanceDisplay(object):
    def __init__(self, distances, size=[300, 60], fast=False):
        self.distances = distances
        self.size = size
        if not fast:
            self.scaleBar = scaleBar(width=size[0] * 3, height=size[1] * 3)
        else:
            self.scaleBar = scaleBar(width=size[0], height=size[1])

    def fastDraw(self, frame):
        temp = self.scaleBar.draw(self.distances.getDistance(frame), sigma=self.distances.getSigma(frame))
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 17)
        draw.text((10, 10), "%0.1f(%0.1f)" % (self.distances.getDistance(frame), self.distances.getSigma(frame)),
                  (0, 0, 0, 255), font=font)
        return temp

    def draw(self, frame, fast=False):
        if fast:
            return self.fastDraw(frame)
        else:
            return self.slowDraw(frame)

    def slowDraw(self, frame):
        temp = self.scaleBar.draw(self.distances.getDistance(frame), sigma=self.distances.getSigma(frame))
        draw = PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 50)
        draw.text((10, 10), "%0.1f(%0.1f)" % (self.distances.getDistance(frame), self.distances.getSigma(frame)),
                  (0, 0, 0, 255), font=font)
        img_resized = temp.resize(self.size, PIL.Image.ANTIALIAS)
        return img_resized


class scaleBar(object):
    def __init__(self, minValue=0, maxValue=200, badValue=150, width=300, height=60):
        self.width = width
        self.height = height
        self.minValue = minValue
        self.maxValue = maxValue
        self.badValue = badValue
        self.delta = maxValue - minValue
        self.badWidth = 1. * (self.badValue - self.minValue) / self.delta * self.width

    def draw(self, value, sigma=0.):
        temp = PIL.Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        width = 1. * (value - self.minValue) / self.delta * self.width
        widthSigma = sigma / self.delta * self.width
        draw = PIL.ImageDraw.Draw(temp)
        if value < self.badValue:
            fColor = (255, 0, 0, 150)
        else:
            fColor = (0, 180, 0, 150)
        draw.rectangle([self.width - width, 0, self.width, self.height / 2], fill=fColor)
        draw.rectangle([0, 0, self.width - width, self.height / 2], fill=(255, 255, 255, 150))
        draw.line((self.width - width, 0, self.width - width, self.height / 2), fill=(255, 255, 255, 200),
                  width=int(widthSigma) + 1)
        draw.line((self.width - self.badWidth, 0, self.width - self.badWidth, self.height / 2 + 16),
                  fill=(0, 0, 0, 200), width=3)

        return temp
