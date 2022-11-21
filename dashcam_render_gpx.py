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
transcoder = actioncam_overlay.AvconvTranscoder("testdata/20171119_123225.MOV", "test.avi", fps=30)
logger.info("# transcoder initialized")
logger.info("# video size: %dx%d" % (transcoder.width, transcoder.height))
start_datetime = datetime.datetime(2017, 11, 19,    hour=12, minute=32, second=48) - datetime.timedelta(hours=1)
start_movietime = datetime.timedelta(seconds=33.5)
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

while True:
    currentFrame += 1
    logger.info("frame {}".format(currentFrame))
    currentImage = transcoder.read_frame()
    try:
        if abs(float(gpscoords.lonF(currentFrame)) - lastlon) > 0.007 or \
                        abs(float(gpscoords.latF(currentFrame)) - lastlat) > 0.007:
            lastlon = float(gpscoords.lonF(currentFrame))
            lastlat = float(gpscoords.latF(currentFrame))
            logger.info("{}, {}".format(lastlat, lastlon))
            mapPlotter = actioncam_overlay.mapPlotter(mapfile="asdf", size=4096, latLonWidth=.01, centerLat=lastlat,
                                                      centerLon=lastlon)
        if not currentFrame % 30:
            previous_points[0].append(float(gpscoords.latF(currentFrame)))
            previous_points[1].append(float(gpscoords.lonF(currentFrame)))
        overlayMap = mapPlotter.plotMapLatLon(float(gpscoords.lonF(currentFrame)), float(gpscoords.latF(currentFrame)),
                                              previousPoints=previous_points)
        currentImage.paste(overlayMap, (0, 0), mask=overlayMap)
        print
        overlayVelocity = velocityDisplay.draw(int(currentFrame), fast=fast)
        currentImage.paste(overlayVelocity, (transcoder.width / 2 - 100, transcoder.height - 60), overlayVelocity)
        overlayTemperature = temperatureDisplay.draw_value_fast(gpscoords.tempF(int(currentFrame)))
        currentImage.paste(overlayTemperature, (transcoder.width - 200, 0), overlayTemperature)
        overlayHeartRate = heartRateDisplay.draw_value_fast(gpscoords.hrF(int(currentFrame)))
        currentImage.paste(overlayHeartRate, (transcoder.width - 200, 60), overlayHeartRate)
        overlayCadence = cadenceDisplay.draw_value_fast(gpscoords.cadF(int(currentFrame)))
        currentImage.paste(overlayCadence, (transcoder.width - 200, 120), overlayCadence)
        #overlayRPM = wheelRPM.draw(int(currentFrame))
        #currentImage.paste(overlayRPM, (transcoder.width - 200, 180), overlayRPM)

    except ValueError:
        pass
        #   overlayDistance = distanceDisplay.draw(int(currentFrame), fast=fast)
        #   currentImage.paste(overlayDistance, (transcoder.width / 2 - 300, transcoder.height / 2), overlayDistance)
        #    overlayTemperature = temperatureDisplay.draw(int(currentFrame), fast=fast)
        #   currentImage.paste(overlayTemperature, (transcoder.width - 200, 0), overlayTemperature)
        #   overlayHeartRate = heartRateDisplay.draw(int(currentFrame), fast=fast)
        #   currentImage.paste(overlayHeartRate, (transcoder.width - 200, 60), overlayHeartRate)
        #   overlayCadence = cadenceDisplay.draw(int(currentFrame))
        #   currentImage.paste(overlayCadence, (transcoder.width - 200, 120), overlayCadence)
        #   overlayRPM = wheelRPM.draw(int(currentFrame))
        #   currentImage.paste(overlayRPM, (transcoder.width - 200, 180), overlayRPM)
    transcoder.write_frame(currentImage)
# if currentFrame>1000:
#        break
