import numpy
from mapnik import *
import mapnik
import Image
import pylab
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import string
import matplotlib.cm as cm
from math import tan, pi
import subprocess
import PIL
import PIL.ImageDraw
import PIL.ImageOps
import subprocess as sp
import json
import cPickle as pickle
from scipy.interpolate import interp1d
from PIL import ImageFont
from pylab import *
import PIL
import PIL.ImageDraw
import PIL.ImageOps
import subprocess as sp

plot(numpy.arange(0, max(x)), speedF(numpy.arange(0, max(x))))
plot(x, speeds, 'ro')

# %pylab inline

FFMPEG_BIN = "avconv"
command = [FFMPEG_BIN,
           '-i', "matze.h264",
           #         '-c:v','h264',
           '-f', "rawvideo",
           '-pix_fmt', 'rgb24',
           '-v', 'debug',
           '-vcodec', "rawvideo", '-']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 9)
command = [FFMPEG_BIN,
           '-y',  # (optional) overwrite output file if it exists
           '-f', 'rawvideo',
           #    '-vcodec','rawvideo',
           '-s', '1296x972',  # size of one frame
           '-pix_fmt', 'rgb24',
           '-r', '25',  # frames per second
           '-i', '-',  # The imput comes from a pipe
           '-an',  # Tells FFMPEG not to expect any audio
           '-c:v', 'h264',
           '-v', 'debug',
           'noTimelapse.avi']

pipeout = sp.Popen(command, stdin=sp.PIPE)

# print len(rawdata)
# rawdata=pipe.stdout.read(1000*1000*3)
# print "lollinger "
# print len(rawdata)
frame = 1
testMap = mapPlotter()
velocityD = velocityDisplay(speedF)
imshow(velocityD.draw(100))
figure()
while True:
    try:
        rawdata = pipe.stdout.read(1296 * 972 * 3)
        raw_image = numpy.fromstring(rawdata, dtype='uint8').reshape((972, 1296, 3))
        videoFrame = PIL.Image.fromarray(raw_image)
        overlayImage = testMap.plotMapLatLon(float(lonF(frame)), float(latF(frame)))
        videoFrame.paste(overlayImage, (0, 0), mask=overlayImage)
        overlayImage = velocityD.draw(int(frame))
        videoFrame.paste(overlayImage, (videoFrame.size[0] / 2 - 100, videoFrame.size[1] - 60), mask=overlayImage)
        pipeout.stdin.write(np.asarray(videoFrame).tostring())
        frame = frame + 1
    # for j in arange(24):
    #            rawdata=pipe.stdout.read(1296*972*3)
    # raw_image = numpy.fromstring(rawdata,dtype='uint8').reshape((972,1296,3))
    #            frame=frame+1
    except:
        print
        "Unexpected error:", sys.exc_info()[0]
        print
        "erreur"
        pipeout.send_signal(2)
        pipe.send_signal(2)
        break
print
frame
print
"done"
pipeout.send_signal(2)
pipe.send_signal(2)
pipeout.send_signal(9)
pipe.send_signal(9)
pylab.rcParams['figure.figsize'] = (20.0, 20)
imshow(videoFrame)
