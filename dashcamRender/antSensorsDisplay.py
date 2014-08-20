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

class arrayValueDisplay(object):
    def __init__(self,valueArray,size=[200,60],symbolBefore=u"",symbolAfter=u""):
        self.array=valueArray
        self.size=size
        self.symbolBefore=symbolBefore
        self.symbolAfter=symbolAfter
        self.initCanvas()
    def initCanvas(self):
        self.emptyCanvas = PIL.Image.new('RGBA', (self.size[0]*3,self.size[1]*3), (255, 255, 255, 128))
        if hasattr(self,"caption"):
            draw=PIL.ImageDraw.Draw(self.emptyCanvas)
            captionFont = PIL.ImageFont.truetype("Arial_Black.ttf", int(45))
            draw.text((0, -5), self.caption, (0,0,0,255), font=captionFont)
        self.smallCanvas=self.emptyCanvas.resize(self.size,PIL.Image.ANTIALIAS)

    def draw(self,frame,fast=False):
        if frame<0:
            frame=0
        if frame >=len(self.array):
            frame=len(self.array)-1
        if not fast: return self.drawValue(self.array[frame])
        elif fast: return self.drawValueFast(self.array[frame])
    def drawValueFast(self,value):
        temp=self.smallCanvas.copy()
        draw=PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Arial.ttf", 50)
        if hasattr(self,"caption"):
            draw.text((0, 8), "%s%d%s" % (self.symbolBefore,value,self.symbolAfter), (0,0,0,255), font=font)
        else:
            draw.text((5, 0), "%s%d%s" % (self.symbolBefore,value,self.symbolAfter), (0,0,0,255), font=font)
        return temp
    def drawValue(self,value):
        temp=self.emptyCanvas.copy()
        draw=PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Arial.ttf", 150)
        if hasattr(self,"caption"):
            draw.text((0, 25), "%s%d%s" % (self.symbolBefore,value,self.symbolAfter), (0,0,0,255), font=font)
        else:
            draw.text((15, 0), "%s%d%s" % (self.symbolBefore,value,self.symbolAfter), (0,0,0,255), font=font)

        img_resized = temp.resize(self.size, PIL.Image.ANTIALIAS)
        return img_resized
    
class heartRateDisplay(arrayValueDisplay):
    def __init__(self,speedF,size=[200,60]):
        self.caption="HEART RATE"
        super(heartRateDisplay,self).__init__(speedF,size,symbolBefore=u"\u2665 ",symbolAfter="")
class sensorVelocityDisplay(arrayValueDisplay):
    def __init__(self,speedF,size=[200,60]):
        self.caption="SPEED"
        super(sensorVelocityDisplay,self).__init__(speedF*60*2.136/1000.,size,symbolBefore=u"",symbolAfter=" km/h")
class cadenceDisplay(arrayValueDisplay):
    def __init__(self,speedF,size=[200,60]):
        self.caption="CADENCE"
        super(cadenceDisplay,self).__init__(speedF,size,symbolBefore="",symbolAfter="/min")
class temperatureDisplay(arrayValueDisplay):
    def __init__(self,speedF,size=[200,60]):
        self.caption="TEMPERATURE"
        super(temperatureDisplay,self).__init__(speedF,size,symbolBefore=u"",symbolAfter=u" \u00B0C")
