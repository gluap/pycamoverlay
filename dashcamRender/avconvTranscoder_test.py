'''
Created on Jul 8, 2014

@author: paulg
'''
import unittest
import avconvTranscoder


class Test(unittest.TestCase):
    def test1(self):
        transcoder = avconvTranscoder.AvconvTranscoder("/home/paulg/my_video.h264", "/tmp/out.h264")
        for i in range(0, 25):
            transcoder.write_frame(transcoder.read_frame())
        transcoder.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
