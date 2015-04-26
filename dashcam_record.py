#!/usr/bin/python
import picamera
import dashcam
maxframes=25*60*360
import dashcamData
import random
import time
debugging=True
print "starting ant sensor"
antSensor=dashcam.antSensors()
randint=int(random.random()*50000000)

#print "sleeping 5 seconds to allow ant sensor system to start" 
time.sleep(5)

#distanceStore=dashcamData.distanceData(False,outFilename="/data/%d.dst" % randint)
antSensorStore=dashcamData.antData(False,outFilename="/data/%d.ant" % randint)



#distanceSensor=dashcam.distanceMeter()
#distanceSensor.start()

camera=picamera.PiCamera()
camera.resolution = (1296,972)
camera.start_recording('/data/%d.h264' % randint,bitrate=0,quantization=25)
camera.ISO=800
camera.video_stabilization=1
framepositions={}
lastIndex=10
lastLat=0

gpsc = dashcam.gpsController()
trackStore=dashcamData.gpsData()
gpsc.start()

while True:
    try:
        if not gpsc.fix.mode==1 and gpsc.fix.latitude!=lastLat:
            print camera.frame.index
            lastLat=gpsc.fix.latitude
            trackStore.addPosition(camera.frame.index,gpsc.fix.latitude,gpsc.fix.longitude,gpsc.fix.speed,gpsc.fix.track,gpsc.utc)
            trackStore.dump("/data/%d.track" % randint)
            if debugging:
                print "ant: %f %f %f %f distance %f" % (antSensor.heartRate,antSensor.wheelRPM,antSensor.cadence,antSensor.temperature,distanceSensor.distance)
        camera.wait_recording(.02)
        if camera.frame.index>lastIndex:
#            distanceStore.addDistance(camera.frame.index,distanceSensor.distance,distanceSensor.deviation)
            #print distanceSensor.distance
            lastIndex=camera.frame.index
            antSensorStore.addData(camera.frame.index,antSensor.heartRate,antSensor.wheelRPM,antSensor.cadence,antSensor.temperature)
            print antSensor.temperature
        if camera.frame.index>maxframes:
            camera.stop_recording()
            trackStore.stopController()
            gpsc.stopController()
            antSensor.stop()
            trackStore.join()
            gpsc.join()
            break
    except KeyboardInterrupt:
        camera.stop_recording()
        gpsc.stopController()
        gpsc.join()
#        distanceStore.close()
#        distanceSensor.stopController()
#        distanceSensor.join()
        antSensor.stop()
        antSensor.join()
        break
    except:
        camera.stop_recording()
        gpsc.stopController()
        gpsc.join()
#        distanceStore.close()
##        distanceSensor.stopController()
#        distanceSensor.join()
        antSensor.stop()
        antSensor.join()
        break
