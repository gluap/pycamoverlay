'''
Created on Jul 7, 2014

@author: paulg
'''
import PIL
import PIL.Image
import subprocess,re
import numpy
import time
import os.path
from distutils.spawn import find_executable
if find_executable('avconv') is None:
    if find_executable('ffmpeg') is None:
        raise EnvironmentError("You need to have avconv or ffmpeg installed in order for dashcamRender to work")
    else:
        avconvBinary=find_executable('ffmpeg')
else:
    avconvBinary=find_executable('avconv')
class avconvTranscoder(object):
    '''
    class to transcode using ffmpeg
    '''


    def __init__(self,infile,outfile):
        '''
        Constructor
        '''
        self.findResolution(infile)
        self.initReader(infile)
        self.initWriter(outfile)
    def findResolution(self,infile):
        if os.path.isfile(infile):
            self.width, self.height=getSize(infile)
            print self.width
            print self.height
            if self.width==0 or self.height==0:
                raise Exception("avconv could not determine input resolution")
        else:
            raise IOError("input file %s does not exist" % infile)
    def initReader(self,infile):
        command=[ avconvBinary,
         '-i', infile,
#         '-c:v','h264',
         '-f', "rawvideo",
         '-pix_fmt','rgb24',
         '-v','quiet',
         '-vcodec', "rawvideo",'-']
        self.avconvIn=subprocess.Popen(command,stdout=subprocess.PIPE, bufsize=10**9)
    def initWriter(self,outfile):
        command = [ avconvBinary,
                   '-y', # (optional) overwrite output file if it exists
                   '-f', 'rawvideo',
                   '-s', '%dx%d' % (self.width,self.height), # size of one frame
                   '-pix_fmt', 'rgb24',
                   '-r', '25', # frames per second
                   '-i', '-', # The imput comes from a pipe
                   '-an', # Tells FFMPEG not to expect any audio
                   '-c:v', 'h264',
                   '-v','quiet',
                   outfile]
        self.avconvOut = subprocess.Popen( command, stdin=subprocess.PIPE)
    def readImage(self):
        rawdata=self.avconvIn.stdout.read(self.width*self.height*3)
        raw_image = numpy.fromstring(rawdata,dtype='uint8').reshape((self.height,self.width,3))
        returnImage= PIL.Image.fromarray(raw_image)
        return returnImage
    def writeImage(self,videoFrame):
        if videoFrame.size[0]==self.width and videoFrame.size[1]==self.height:
            self.writeNumpyArray(numpy.asarray(videoFrame))
        else:
            raise Exception("you should only save images of %dx%d, but you tried %dx%d" % (self.width,self.height,videoFrame.size[0],videoFrame.size[1]))
    def writeNumpyArray(self,rawNumpyData):
        self.avconvOut.stdin.write(rawNumpyData.tostring())
    def __del__(self):
        self.avconvIn.send_signal(2)
       # self.avconvIn.terminate()
       # self.avconvIn.kill()
#        self.avconvOut.send_signal(2)
       # self.avconvOut.terminate()
       # self.avconvOut.kill()
    def close(self):
        self.__del__()

def getSize(pathtovideo):
    pattern = re.compile(r'Stream.*Video.*\s([0-9]+)x([0-9]{3})')
    p = subprocess.Popen([avconvBinary, '-i', pathtovideo],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    match = pattern.search(stderr)
    print match.groups()
    if match:
        x, y = map(int, match.groups()[0:2])
    else:
        x = y = 0
    return x, y