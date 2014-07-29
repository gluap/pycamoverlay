import dashcam
testm=dashcam.distanceMeter()
testm.start()
import time
while True:
    try:
        print "%f +-%f" % (testm.distance, testm.deviation)
        time.sleep(.1)
    except KeyboardInterrupt:
        testm.stopController()
        testm.join()
        break
