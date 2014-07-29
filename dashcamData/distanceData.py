import numpy
class distanceData():
    def __init__(self,inFilename,outFilename=False):
        if outFilename:
            self.lastFrame=0
            self.distanceFile=open(outFilename,"wb")
        elif inFilename is not None:
            self.initFromFile(inFilename)
        else:
            raise Exception("you should either provide outFilename or inFilename")
        
    def addDistance(self,frame,distance,sigma):
        if(frame-1>self.lastFrame and frame!=1):
            self.addDistance(frame-1,distance,sigma)
        tempdistance=[distance,sigma]
        self.lastFrame=frame
        self.distanceFile.write(numpy.array(tempdistance,dtype=float).tostring())
    def close(self):
        self.distanceFile.close()
    def initFromFile(self,filename):
        self.distances,self.sigmas=numpy.fromfile(filename,dtype="float").reshape((-1,2)).T
    def getDistance(self,frame):
        if frame<=0:
            frame=1
        if frame>len(self.distances):
            frame=len(self.distances)+1
        return self.distances[frame-1]
    def getSigma(self,frame):
        if frame<=0:
            frame=1
        if frame>len(self.distances):
            frame=len(self.distances)+1
        return self.sigmas[frame-1]