import sys
import time
from ant.core import driver, node, event, message, log
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER
import struct

class heartRateCallback(event.EventCallback):
    def __init__(self):
        self.heartRate=0
        self.beatCount=0
        self.lastBeat=0
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            self.heartRate = ord(msg.payload[-1])
            self.beatCount = ord(msg.payload[-2])
            self.lastBeat = struct.unpack('<H',"".join(msg.payload[-4:-2]))[0]/1024.
    def start(self,antnode):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:HRM'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(120, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8070)
        self.channel.setFrequency(57)
        self.channel.open()
        self.channel.registerCallback(self)
    def stop(self):
            self.channel.close()
            self.channel.unassign()

class temperatureCallback(event.EventCallback):
    def __init__(self):
        self.temperature=0
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            if ord(msg.payload[0])==1:
                tempTemperature= struct.unpack('<h',"".join(msg.payload[-2:]))[0]*0.01
                if tempTemperature!=0:
                    self.temperature=tempTemperature
    def start(self,antnode):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:TEM'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(25, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8192)
        self.channel.setFrequency(57)
        self.channel.open()
        self.channel.registerCallback(self)
    def stop(self):
        self.channel.close()
        self.channel.unassign()

class cadenceCallback(event.EventCallback):
    def __init__(self,circ=2.136):
        '''
        to calculate speed from RPM give the circumference of the wheel.
        '''
        self.cadence=0
        self.pedalRevolutions=0
        self.wheelRevolutions=0
        self.wheelRPM=0
        self.speed=0
        self.lastPedalTime=0.
        self.lastWheelTime=0.
        self.wheelCircumference=circ
    def start(self,antnode):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:CDM'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(121, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8086)
        self.channel.setFrequency(57)
        self.channel.open()
        self.channel.registerCallback(self)
    def stop(self):
        self.channel.close()
        self.channel.unassign()
    def process(self,msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            (cadenceTime,cadenceRev,wheelTime,wheelRevolutions)=struct.unpack("<H","".join(msg.payload[-8:]))
            cadenceTime/=1024
            wheelTime/=1024
            if wheelTime<self.lastWheelTime:
                lastWheelTime-=64
            if pedalTime<self.lastPedalTime:
                pedalTime-=64
            if wheelRevolutions < self.wheelRevolutions:
                self.wheelRevolutions-=65536
            if pedalRevolutions < self.pedalRevolutions:
                self.pedalRevolutions-=65536 
            self.wheelRPS=(pedalRevolutions-self.pedalRevolutions)/(pedalTime-self.lastPedalTime)*60
            self.cadence=(wheelRevolutions-self.wheelRevolutions)/(wheelTime-self.lastWheelTime)*60
            self.speed=self.wheelRPS*self.wheelCircumference*3600
            self.lastWheelTime=wheelTime
            self.lastPedalTime=pedalTIme
            self.wheelRevolutions=wheelRevolutions
            self.pedalRevolutions=pedalRevolutions

class antDevices():
    def __init__(self):
        self.stick = driver.USB2Driver('/dev/ttyUSB0')
        self.antnode = node.Node(self.stick)
        self.antnode.start()
        self.key = node.NetworkKey('N:ANT+', 'B9A521FBBD72C345'.decode('hex'))
        self.antnode.setNetworkKey(0, self.key)
        self.devices=[]
    def add_device(self,device):
        device.start(self.antnode)
        self.devices.append(device)
    def stop(self):
        for device in self.devices:
            device.stop()
        self.antnode.stop()
    def __exit__(self):
        self.stop()


class antSensors():
    def __init__(self):
        self.myMonitors=antDevices()
        self.HRM=heartRateCallback()
        self.myMonitors.add_device(self.HRM)
        self.TEM=temperatureCallback()
        self.myMonitors.add_device(self.TEM)
        self.CDM=cadenceCallback()
        self.myMonitors.add_device(self.CDM)
    def __exit__(self):
        self.myMonitors.stop()
    def stop(self):
        self.myMonitors.stop()
    @property
    def heartRate(self):
        return self.HRM.heartRate
    @property
    def cadence(self):
        return self.CDM.cadence
    @property
    def wheelRPM(self):
        return self.CDM.wheelRPM
    @property
    def temperature(self):
        return self.TEM.temperature