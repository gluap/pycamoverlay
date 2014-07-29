'''
Created on Jul 6, 2014

@author: paulg
'''
import PIL
import PIL.ImageFont
class gpsVelocityDisplay:
    def __init__(self,speedF,size=[200,60]):
        self.speed=speedF
        self.size=size
        self.canvas= PIL.Image.new('RGBA', (self.size[0]*3,self.size[1]*3), (255, 255, 255, 128))
        self.smallCanvas=PIL.Image.new('RGBA', (self.size[0],self.size[1]), (255, 255, 255, 128))
    def fastDraw(self,frame):
        temp = self.smallCanvas.copy()
        draw=PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 50)
        draw.text((10, 0), "%d km/h" % (int(self.speed(frame)*3.6)), (0,0,0,255), font=font)
        return temp
    def draw(self,frame,fast=False):
        if fast:
            return self.fastDraw(frame)
        temp = self.canvas.copy()
        draw=PIL.ImageDraw.Draw(temp)
        font = PIL.ImageFont.truetype("Ubuntu-C.ttf", 150)
        draw.text((10, 0), "%d km/h" % (int(self.speed(frame)*3.6)), (0,0,0,255), font=font)
        img_resized = temp.resize(self.size, PIL.Image.ANTIALIAS)
        return img_resized