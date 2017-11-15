#!/usr/bin/python
#import picamera
import dashcam
maxframes=25*60*360
import dashcamData
import random
import time

antSensor=dashcam.AntSensors()
print "sleeping 5 seconds to allow ant sensor system to start" 
time.sleep(5)
randint=1
#distanceStore=dashcamData.distanceData(False,outFilename="/data/%d.dst" % randint)
antSensorStore=dashcamData.antData(False,outFilename="%d.ant" % randint)
i=0
while True:
    try:
        i+=1
#        antSensorStore.addData(i,antSensor.heartRate,antSensor.wheelRPM,antSensor.cadence,antSensor.temperature)
        print "cadence=%f rpm=%f" %(antSensor.cadence,antSensor.wheel_rpm)
        print "revolutions: c=%f, w=%f" % (antSensor.CDM.wheelRevolutions,antSensor.CDM.pedalRevolutions)
        print "heart %d beatcount %d last %d" % (antSensor.heartrate, antSensor.HRM.beatCount, antSensor.HRM.lastBeat)
        print "temperature %f" % (antSensor.temperature)
        time.sleep(1)
#            print antSensor.temperature
    except KeyboardInterrupt:

        antSensor.stop()
        break
