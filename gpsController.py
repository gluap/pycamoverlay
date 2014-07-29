'''
Created on Jul 8, 2014

@author: paulg
'''
import gps
import threading

# culd be beefed up with code from here http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#GPS
class gpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps.gps(mode=gps.WATCH_ENABLE) #starting the stream of info
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False
  
    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites
