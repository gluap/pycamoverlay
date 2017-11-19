'''
Created on Jul 6, 2014

@author: paulg
'''
import mapnik
import numpy
import math
import PIL
import PIL.ImageDraw
import subprocess
import logging
import requests
import StringIO
logger=logging.getLogger(__name__)

class mapDisplay:
    def __init__(self):
        print("inited")

    def draw(self, frame):
        print("should draw")


class mapPlotter:
    def __init__(self, mapfile='osmt.xml', map_output='mymap.png', latLonWidth=.025, centerLat=49.88, centerLon=8.67,
                 size=4 * 1024):
        self.m = mapnik.Map(size, size)
        self.m.srs=("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over")
        self.merc = mapnik.Projection(self.m.srs)
        self.longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        self.transform = mapnik.ProjTransform(self.longlat, self.merc)
        bbox_latlon = (mapnik.Envelope(centerLon - latLonWidth, centerLat - latLonWidth, centerLon + latLonWidth,
                                       centerLat + latLonWidth))
        bbox = self.transform.forward(bbox_latlon)
        self.m.zoom_to_box(bbox)
        envelope = self.m.envelope()
        envelope_numbers = envelope.__getinitargs__()
        self.xl, self.yl = (envelope_numbers[0], envelope_numbers[1])
        self.xh, self.yh = (envelope_numbers[2], envelope_numbers[3])
        image = requests.get("http://oldweb.das-konnektiv.de:5000/map/{lat}/{lon}/{width}/{size}".format(
            lat=centerLat, lon=centerLon, width=latLonWidth, size=size))
        logger.info(image)

        self.mapImage = PIL.Image.open(StringIO.StringIO(image.content))

    def plotMapLatLon(self, lon, lat, previousPoints=False):
        x, y = self.latLonToXY(lon, lat)
        img = self.plotMap(x, y)
        if previousPoints:
            draw = PIL.ImageDraw.Draw(img)
            x1, y1 = self.calcPos(x, y)
            coords = self.calcPolygonCoords(previousPoints[0], previousPoints[1], shift=[x1 - 150, y1 - 150])
            draw.line(coords.reshape(coords.shape[0] * coords.shape[1]).tolist(), fill=(180, 0, 0, 255), width=5)
        return img

    def latLonToXY(self, lon, lat):
        coord = mapnik.Coord(lon, lat)
        coord_merc = self.transform.forward(coord)
        return coord_merc.x, coord_merc.y

    def plotMap(self, x, y):
        x1, y1 = self.calcPos(x,y)
        tempImage = self.mapImage.crop([int(x1) - 150, int(y1) - 150, int(x1) + 150, int(y1) + 150])
        draw = PIL.ImageDraw.Draw(tempImage)
        draw.ellipse((145, 145, 155, 155), fill=(180, 0, 0, 255))
        return tempImage  # .crop([int(x1)-100,int(y1)-100,int(x1)+100,int(y1)+100])

    def calcPosRel(self, x1, y1):
        xrel, yrel = ((x1 - self.xl) / (self.xh - self.xl), 1 - (y1 - self.yl) / (self.yh - self.yl))
        return xrel, yrel

    def calcPos(self, x, y):
        xrel, yrel = self.calcPosRel(x, y)
        return xrel * self.mapImage.size[0], yrel * self.mapImage.size[1]

    def calcPolygonCoords(self, lats, lons, shift=[0, 0]):
        coords = numpy.array([lats, lons]).T
        coordsnew = numpy.zeros(coords.shape)
        for i in numpy.arange(coords.shape[0]):
            xtemp, ytemp = self.latLonToXY(coords[i][1], coords[i][0])
            coordsnew[i] = self.calcPos(xtemp, ytemp)
            coordsnew[i] = coordsnew[i] - numpy.array(shift)
        return coordsnew

    def plotPolygon(self, lats, lons):
        coords = self.calcPolygonCoords(lats, lons)
        tempImage = self.mapImage.copy()
        draw = PIL.ImageDraw.Draw(tempImage)
        draw.line(coords.reshape(coords.shape[0] * coords.shape[1]).tolist(), fill=(0, 255, 0, 255), width=5)
        return tempImage
