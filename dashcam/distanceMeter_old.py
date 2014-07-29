'''
Distance meter class in pure python, loosely based on

http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/
http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
http://www.stuffaboutcode.com/2013/09/raspberry-pi-gps-setup-and-python.html

License GPL 
'''
import threading
import RPi.GPIO as GPIO
import time
import numpy
# culd be beefed up with code from here http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#GPS
GPIO_TRIGGER = 23 # trigger pin for firing ultrasound measurement
GPIO_ECHO = 24 # echo pin, the sensor pulls it up for the time it takes the pulse to travel.
class distanceMeter(threading.Thread):
    def __init__(self):
        '''init the sensor'''
        threading.Thread.__init__(self)
        self.setupGPIO()
        self.initializeVariables()
    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(GPIO_ECHO, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
        GPIO.output(GPIO_TRIGGER, False)
    def initializeVariables(self):        
        self.distanceMeasured=100000
        self.standardDeviation=100000
        self.running = False
        self.timeDiff=0
        self.last10=numpy.zeros((10,2))
    def run(self):
        self.flankTime=0.0
        self.running = True
        GPIO.remove_event_detect(GPIO_ECHO)
        GPIO.add_event_detect(GPIO_ECHO,   GPIO.BOTH, callback=self.risingDetected, bouncetime=0)
        i=0
        while self.running:
            currentTotal=0.
            values=numpy.zeros(7)
            i=0
            while i<7:
                GPIO.output(GPIO_TRIGGER, True)
                time.sleep(0.00001)
                GPIO.output(GPIO_TRIGGER, False)
                while self.timeDiff==0:
                    time.sleep(.01)
                if self.timeDiff<1:
                    values[i]=self.timeDiff * 17000.
                    i+=1
                self.timeDiff=0.0
                self.flankTime=0.0
            self.standardDeviation=numpy.std(values)
            self.distanceMeasured=numpy.mean(values)
            self.last10[i%10]=[self.distanceMeasured,self.standardDeviation]
    def risingDetected(self,pin):
        tempTime=time.time()
        if GPIO.input(pin):
            self.flankTime=tempTime
        else: 
            self.timeDiff=tempTime-self.flankTime
#            print self.timeDiff


    def stopController(self):
        self.running = False
    @property
    def deviation(self):
        return self.standardDeviation
    @property
    def distance(self):
        return self.distanceMeasured
if __name__ == '__main__':
    meter=distanceMeter()
    meter.start() # start is implemented in the parent class!
    for i in numpy.arange(0,100):
        try:
            time.sleep(1)
            print "currently measuring %0.3f +- %0.3f" % (meter.distance,meter.deviation)
        except:
            meter.stopController()
            meter.join()
            break
    