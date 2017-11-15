#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import dashcamRender
import dashcamData
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

parser = argparse.ArgumentParser(description='Postprocess dashcam video and data files.')
parser.add_argument('-i', '--infile')
parser.add_argument('-o', '--outfile')
parser.add_argument('-m', '--mapfile')
args = parser.parse_args()
logger.info("# initializing map")

logger.info("# initializing transcoder")
transcoder = dashcamRender.AvconvTranscoder(args.infile + ".h264", args.outfile + ".avi")
logger.info("# transcoder initialized")
logger.info("# video size: %dx%d" % (transcoder.width, transcoder.height))
gpscoords = dashcamData.gpsData(args.infile + ".track")
#distances = dashcamData.distanceData(args.infile + ".dst")
#antData = dashcamData.antData(args.infile + ".ant")
#logger.info(distances.distances)
velocityDisplay = dashcamRender.gpsVelocityDisplay(gpscoords.speedF)
#distanceDisplay = dashcamRender.distanceDisplay(distances, fast=True)
#cadenceDisplay = dashcamRender.cadenceDisplay(antData.cadences)
#temperatureDisplay = dashcamRender.temperatureDisplay(antData.temperatures)
#heartRateDisplay = dashcamRender.heartRateDisplay(antData.heartRates)
#wheelRPM = dashcamRender.sensorVelocityDisplay(antData.wheelRPMs)
fast = True
currentFrame = 0
lastlon = 0
lastlat = 0
while True:
    currentFrame += 1
    logger.info("frame {}".format(currentFrame))
    currentImage = transcoder.read_frame()
    try:
        if abs(float(gpscoords.lonF(currentFrame)) - lastlon) >0.05 or   \
                        abs(float(gpscoords.latF(currentFrame))-lastlat)>0.05:
            lastlon = float(gpscoords.lonF(currentFrame))
            lastlat = float(gpscoords.latF(currentFrame))
            logger.info("{}, {}".format(lastlat,lastlon))
            mapPlotter = dashcamRender.mapPlotter(mapfile=args.mapfile, size=1024, latLonWidth=.01, centerLat=lastlat,
                                                  centerLon=lastlon)

        overlayMap = mapPlotter.plotMapLatLon(float(gpscoords.lonF(currentFrame)),float(gpscoords.latF(currentFrame)))
        currentImage.paste(overlayMap, (0, 0), mask=overlayMap)
        overlayVelocity = velocityDisplay.draw(int(currentFrame), fast=fast)
        currentImage.paste(overlayVelocity, (transcoder.width / 2 - 100, transcoder.height - 60), overlayVelocity)
    except ValueError:
        pass
 #   overlayDistance = distanceDisplay.draw(int(currentFrame), fast=fast)
 #   currentImage.paste(overlayDistance, (transcoder.width / 2 - 300, transcoder.height / 2), overlayDistance)
 #   overlayTemperature = temperatureDisplay.draw(int(currentFrame), fast=fast)
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
