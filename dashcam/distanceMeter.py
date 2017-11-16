from __future__ import print_function, unicode_literals, division, absolute_import

'''
Created on Jul 8, 2014

@author: paulg
'''
import threading
import subprocess
import time
import numpy
import os


# from xdg.Menu import tmp
# culd be beefed up with code from here http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
# GPS


class distanceMeter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.distanceProcess = subprocess.Popen(['./distance'], stdout=subprocess.PIPE, bufsize=500,
                                                preexec_fn=lambda: os.nice(-19))
        self.running = True
        self.currentdistance = 0.0
        self.lastFive = numpy.zeros(5)
        self.lastFiveValid = numpy.zeros(5)
        self.current = 0.
        self.currentValid = 0.
        self.currentDistance = 0.
        print("created")

    def run(self):
        print("starting loop")
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            #         try:
            rawdata = self.distanceProcess.stdout.read(4)
            tmp = numpy.fromstring(rawdata, dtype="<f4")[-1]
            if (numpy.abs(self.lastFive - tmp) < 5).any():
                #      print self.lastFive
                self.currentDistance = tmp
                self.lastFiveValid[self.currentValid % 5] = tmp
                self.currentValid += 1
            self.lastFive[self.current % 5] = tmp
            self.current += 1
        #            except IndexError:
        #                print "strange, distance data coming in too slow?"
        #                pass

    def stopController(self):
        self.running = False
        self.distanceProcess.send_signal(2)
        self.distanceProcess.kill()

    @property
    def distanceMean(self):
        return numpy.mean(self.lastFiveValid)

    @property
    def deviation(self):
        return numpy.std(self.lastFiveValid)

    @property
    def distance(self):
        return self.currentDistance


if __name__ == '__main__':
    test = distanceMeter()
    test.start()
    for i in numpy.arange(1000):
        try:
            print(test.distance)
            time.sleep(.1)
        except KeyboardInterrupt:
            test.stopController()
            test.join()
            break
