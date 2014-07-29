'''
Created on Jul 7, 2014

@author: paulg
'''
import unittest
from gpsData import gpsData

class Test(unittest.TestCase):
    def testAddPosition1(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 3, "time")
        self.assertEqual(gpsTrack.lats[0],0)
        self.assertEqual(gpsTrack.lons[0],1)
        self.assertEqual(gpsTrack.speeds[0],0)
        self.assertEqual(gpsTrack.tracks[0],3)
        self.assertEqual(gpsTrack.times[0],"time")
        self.assertEqual(len(gpsTrack.tracks),1)
        gpsTrack.addPosition(0, 2, 3, 4, 5, "time2")
        self.assertEqual(gpsTrack.frames[1],0)        
        self.assertEqual(gpsTrack.lats[1],2)
        self.assertEqual(gpsTrack.lons[1],3)
        self.assertEqual(gpsTrack.speeds[1],4)
        self.assertEqual(gpsTrack.tracks[1],5)
        self.assertEqual(gpsTrack.times[1],"time2")
        self.assertEqual(len(gpsTrack.tracks),2)
        gpsTrack.addPosition(0, float('nan'), 3, 4, 5, "time2")
        self.assertEqual(len(gpsTrack.tracks),2)
    def testPickle1Point(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 3, "time")
        self.assertRaises(Exception, gpsTrack.dump,"test.pickle", "one point storing should raise exception")
    def testPickle(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 2, "time")
        gpsTrack.addPosition(10, 1, 0, 1, -1, "time")
        gpsTrack.dump("test.pickle")
        blub=gpsData(inputfile="test.pickle")
        self.assertEqual(blub.latF(5),0.5)
        self.assertEqual(blub.lonF(5),0.5)
        self.assertEqual(blub.speedF(5),0.5)
        self.assertEqual(blub.trackF(5),0.5)
    def testInterpolation(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 2, "time")
        gpsTrack.addPosition(10, 1, 0, 1, -1, "time")
        gpsTrack.buildInterpolations()
        self.assertEqual(gpsTrack.latF(5),0.5)
        self.assertEqual(gpsTrack.lonF(5),0.5)
        self.assertEqual(gpsTrack.speedF(5),0.5)
        self.assertEqual(gpsTrack.trackF(5),0.5)
        gpsTrack.dump("test.pickle")
        self.assertEqual(gpsTrack.latF(5),0.5)
    def testNoInterpolation(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 2, "time")
        gpsTrack.addPosition(10, 1, 0, 1, -1, "time")
        self.assertTrue(not hasattr(gpsTrack,'latF'))
    def testInterpolationUpdates(self):
        gpsTrack=gpsData()
        gpsTrack.addPosition(0, 0, 1, 0, 2, "time")
        gpsTrack.addPosition(10, 1, 0, 1, -1, "time")
        gpsTrack.buildInterpolations()
        gpsTrack.addPosition(20, 0, 1, 0, 2, "time")
        self.assertEqual(gpsTrack.trackF(15),0.5)
#    def testFrames(self):
#        gpsTrack=gpsData()
#       # gpsTrack.addDistance(,1,0.1)
#        gpsTrack.addDistance(1,2,0.1)
#        gpsTrack.addDistance(4,3,0.1)
#        self.assertEqual(gpsTrack.getDistance(3),3)
#        self.assertEqual(gpsTrack.getDistance(0),2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()