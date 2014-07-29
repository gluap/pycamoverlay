from distanceData import distanceData
import unittest
import numpy

class Test(unittest.TestCase):
    def testAddPosition1(self):
        test=distanceData(outFilename="testfile.npy")
        test.addDistance(1,0,0)
        test.addDistance(10,1,2)
        test.addDistance(15,15,16)
        test.close()
        test2=distanceData(inFilename="testfile.npy")
        self.assertEqual(test2.getDistance(1),0)
        self.assertEqual(test2.getDistance(15),15)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()