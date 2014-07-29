from antData import antData
import unittest
import numpy

class Test(unittest.TestCase):
    def testAddPosition1(self):
        test=antData("",outFilename="testfile.npy")
        test.addData(0,1,2,3,4)
        test.addData(10,11,22,33,44)
        test.addData(15,111,222,333,444)
        test.close()
        test2=antData(inFilename="testfile.npy")
        self.assertEqual(test2.getTemperature(1),44)
        self.assertEqual(test2.getCadence(15),222)
if __name__ == "__main__":
    unittest.main()