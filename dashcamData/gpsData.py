'''
Created on Jul 6, 2014

@author: paulg
'''
import cPickle as pickle
import math

try:
    from scipy.interpolate import interp1d
except ImportError:
    pass


class gpsData(object):
    '''
    this class is used to store GPS data for dashcam video.
    '''

    def __init__(self, inputfile=False):
        '''
        Constructor
        
        '''
        if inputfile:
            self.initFromPickle(inputfile)
            self.buildInterpolations()
        else:
            self.frames = []
            self.lats = []
            self.lons = []
            self.speeds = []
            self.tracks = []
            self.times = []

    def addPosition(self, frame, lat, lon, speed, track, time):
        '''
        This method expects the arguments above. They are stored if frame, lat, lon, speed and track are a number, otherwise nothing is stored.
        '''
        if not math.isnan(frame + lat + lon + speed + track):
            self.frames.append(frame)
            self.lats.append(lat)
            self.lons.append(lon)
            self.speeds.append(speed)
            self.tracks.append(track)
            self.times.append(time)
            if hasattr(self, 'latF'):
                self.buildInterpolations()

    def buildInterpolations(self):
        if len(self.frames) < 2:
            raise Exception("you need to have more than one point for a track.")
        self.latF = interp1d(self.frames, self.lats, kind='linear')
        self.lonF = interp1d(self.frames, self.lons, kind='linear')
        self.speedF = interp1d(self.frames, self.speeds, kind='linear')
        self.trackF = interp1d(self.frames, self.tracks, kind='linear')

    def initFromPickle(self, filename):
        self.__dict__ = pickle.load(open(filename, "r"))

    def dump(self, filename):
        rebuild = False
        if hasattr(self, 'latF'):
            del self.latF
            del self.lonF
            del self.speedF
            del self.trackF
            rebuild = True
        outFH = open(filename, "w")
        pickle.dump(self.__dict__, outFH, 2)
        outFH.close()
        if rebuild:
            self.buildInterpolations()

    def getDistance(self, frame):
        return self.distances[frame]

    def getSigma(self, frame):
        return self.sigmas[frame]
