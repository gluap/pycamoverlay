import numpy
import numpy

class antData():
    def __init__(self,inFilename,outFilename=False):
        if outFilename:
            self.lastFrame=0
            self.distanceFile=open(outFilename,"wb")
        elif inFilename is not None:
            self.initFromFile(inFilename)
        else:
            raise Exception("you should either provide outFilename or inFilename")
        
    def addData(self,frame,heartRate,wheelrpm,cadence,temperature):
        if(frame-1>self.lastFrame and frame!=1):
            self.addData(frame-1,heartRate,cadence,wheelrpm,temperature)
        tempdistance=[heartRate,cadence,wheelrpm,temperature]
        self.lastFrame=frame
        self.distanceFile.write(numpy.array(tempdistance,dtype=float).tostring())
    def close(self):
        self.distanceFile.close()
    def initFromFile(self,filename):
        self.heartRates,self.cadences,self.wheelRPMs,self.temperatures=numpy.fromfile(filename,dtype="float").reshape((-1,4)).T
        print self.heartRates
        print self.temperatures
    def getHeartRate(self,frame):
        return self.getFromArray(frame, self.heartRates)
    def getCadence(self,frame):
        return self.getFromArray(frame, self.cadences)
    def getWheelRPM(self,frame):
        return self.getFromArray(frame, self.wheelRPMs)
    def getSpeed(self,frame):
        return self.getWheelRPM(frame)*60*2.136
    def getTemperature(self,frame):
        return self.getFromArray(frame, self.temperatures)
    def getFromArray(self,frame,inArray):
        if frame<=0:
            frame=0
        if frame>len(inArray):
            frame=len(inArray)
        ret= inArray[frame]
        return ret


