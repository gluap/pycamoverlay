'''
Created on Jul 8, 2014

@author: paulg
'''
import unittest
import actioncam_overlay.avconv_transcoder


class Test(unittest.TestCase):
    def test1(self):
        transcoder = actioncam_overlay.avconv_transcoder.AvconvTranscoder("/home/paulg/Workspace/pidashcam/testdata/3320804.h264", "/tmp/out.h264")
        for i in range(0, 25):
            transcoder.write_frame(transcoder.read_frame())
        transcoder.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
