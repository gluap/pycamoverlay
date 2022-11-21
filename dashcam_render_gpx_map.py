#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import actioncam_overlay
import dashcamData
import datetime
import dashcamData.gpx_data
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Postprocess dashcam video and data files.')

args = parser.parse_args()
logger.info("# initializing map")

logger.info("# initializing transcoder")
# transcoder = actioncam_overlay.AvconvTranscoder("testdata/20171119_123225.MOV", "test.avi", fps=30)
logger.info("# transcoder initialized")
#logger.info("# video size: %dx%d" % (transcoder.width, transcoder.height))
start_datetime = datetime.datetime(2017, 11, 19, hour=12, minute=32, second=48) - datetime.timedelta(hours=1)
start_movietime = datetime.timedelta(seconds=31.1)
gpscoords = dashcamData.gpx_data.GPXdata("testdata/activity_2339617760.gpx", start_movietime, start_datetime, 30)
# distances = dashcamData.distanceData(args.infile + ".dst")
# antData = dashcamData.antData(args.infile + ".ant")
# logger.info(distances.distances)
velocityDisplay = actioncam_overlay.gpsVelocityDisplay(gpscoords.speedF)
# distanceDisplay = actioncam_overlay.distanceDisplay(distances, fast=True)
cadenceDisplay = actioncam_overlay.CadenceDisplay([])
temperatureDisplay = actioncam_overlay.TemperatureDisplay([])
heartRateDisplay = actioncam_overlay.HeartRateDisplay([])
# wheelRPM = actioncam_overlay.sensorVelocityDisplay(antData.wheelRPMs)
fast = True
currentFrame = 0
lastlon = 0
lastlat = 0
previous_points = [[], []]
#mapPlotter = actioncam_overlay.mapPlotter(mapfile="asdf", size=4096, latLonWidth=.03, centerLat=gpscoords._latitudes[0],
#                                          centerLon=gpscoords._longitudes[0])

import PIL
#a= mapPlotter.plotPolygon(gpscoords._latitudes, gpscoords._longitudes)
#a.save("/tmp/test.png","png",optimize=True,quality=9, compress=9)

import numpy
import matplotlib.pyplot as plt
plt.plot(gpscoords._times,gpscoords._hrs)
plt.plot(gpscoords._speeds_times,gpscoords._speeds)
plt.plot(gpscoords._times,gpscoords._alts)


plt.show()
min=min(gpscoords._speeds_times)
max=max(gpscoords._speeds_times)
frames=numpy.arange(30*(max-min))

plt.plot(frames,map(gpscoords.speedF, frames))
print(map(gpscoords._speed_inter,gpscoords._speeds_times))
print(gpscoords._speed_inter(gpscoords.datetime_at_frame(3)))
print(gpscoords.speedF(3))

plt.show()