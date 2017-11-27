'''
Created on Jul 7, 2014

@author: paulg
'''
from __future__ import print_function, absolute_import, division, unicode_literals

import PIL
import PIL.Image
import subprocess, re
import numpy
import os.path
from distutils.spawn import find_executable

if find_executable('avconv') is None:
    if find_executable('ffmpeg') is None:
        raise EnvironmentError("You need to have avconv or ffmpeg installed in order for actioncam_overlay to work")
    else:
        AVCONV_BINARY = find_executable('ffmpeg')
else:
    AVCONV_BINARY = find_executable('avconv')


class AvconvTranscoder(object):
    '''
    class to transcode using ffmpeg
    '''

    def __init__(self, infile, outfile, fps=25):
        '''
        Constructor
        '''
        self.width, self.height = self.find_resolution(infile)
        self.avconv_in = self.init_reader(infile)
        self.avconv_out = self.init_writer(outfile)
        self.fps = fps


    def find_resolution(self, infile):
        if os.path.isfile(infile):
            width, height = get_size(infile)
            print("resolution: {}x{}".format(width, height))
            if width == 0 or height == 0:
                raise Exception("avconv could not determine input resolution")
        else:
            raise IOError("input file %s does not exist" % infile)
        return width, height

    def init_reader(self, infile):
        command = [AVCONV_BINARY,
                   '-i', infile,
                   #         '-c:v','h264',
                   '-f', "rawvideo",
                   '-pix_fmt', 'rgb24',
                   '-v', 'quiet',
                   '-vcodec', "rawvideo", '-']
        return subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10 ** 9)

    def init_writer(self, outfile):
        command = [AVCONV_BINARY,
                   '-y',  # (optional) overwrite output file if it exists
                   '-f', 'rawvideo',
                   '-s', '%dx%d' % (self.width, self.height),  # size of one frame
                   '-pix_fmt', 'rgb24',
                   '-r', str(self.fps),  # frames per second
                   '-i', '-',  # The imput comes from a pipe
                   '-an',  # Tells FFMPEG not to expect any audio
                   '-c:v', 'h264',
                   '-v', 'quiet',
                   outfile]
        return subprocess.Popen(command, stdin=subprocess.PIPE)

    def read_frame(self):
        rawdata = self.avconv_in.stdout.read(self.width * self.height * 3)
        raw_image = numpy.fromstring(rawdata, dtype='uint8').reshape((self.height, self.width, 3))
        return_image = PIL.Image.fromarray(raw_image)
        return return_image

    def write_frame(self, videoFrame):
        if videoFrame.size[0] == self.width and videoFrame.size[1] == self.height:
            self.write_numpy_array(numpy.asarray(videoFrame))
        else:
            raise Exception("you should only save images of %dx%d, but you tried %dx%d" % (
                self.width, self.height, videoFrame.size[0], videoFrame.size[1]))

    def write_numpy_array(self, rawNumpyData):
        self.avconv_out.stdin.write(rawNumpyData.tostring())

    def __del__(self):
        try:
            self.avconv_in.send_signal(2)
        # self.avconvIn.terminate()
        # self.avconvIn.kill()
            self.avconv_out.send_signal(2)
        except AttributeError:
            pass

    def close(self):
        self.__del__()


def get_size(pathtovideo):
    pattern = re.compile(r'Stream.*Video.*\s([0-9]+)x([0-9]{3})')
    p = subprocess.Popen([AVCONV_BINARY, '-i', pathtovideo],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    match = pattern.search(stderr)
    match.groups()
    if match:
        x, y = map(int, match.groups()[0:2])
    else:
        x = y = 0
    return x, y
