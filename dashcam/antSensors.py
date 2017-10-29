import sys
import time
from ant.core import driver, node, event, message, log
from ant.core.node import Node, Network, ChannelID
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER

from ant.core.constants import NETWORK_KEY_ANT_PLUS, NETWORK_NUMBER_PUBLIC
from ant.plus.heartrate import *
import struct
import numpy


class heartRateCallback(event.EventCallback):
    def __init__(self):
        self.heartRate = 0
        self.beatCount = 0
        self.lastBeat = 0

    def process(self, msg, *args):
        print args
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            self.heartRate = ord(msg.payload[-1])
            self.beatCount = ord(msg.payload[-2])
            self.lastBeat = struct.unpack('<H', "".join(msg.payload[-4:-2]))[0] / 1024.

    def start(self, antnode, network):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:HRM'
        self.channel.assign(network, CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(120, 0, 0)
        self.channel.searchTimeout = TIMEOUT_NEVER
        self.channel.period = 8070
        self.channel.frequency = 57
        self.channel.open()
        self.channel.registerCallback(self)

        #    channel = antnode.getFreeChannel()
        # channel.name = 'C:WGT'
        # channel.assign(net, CHANNEL_TYPE_TWOWAY_RECEIVE)
        # channel.setID(119, 0, 0)
        # channel.period = 0x2000  # nebo 0x0020 ???
        # channel.frequency = 0x39

    def stop(self):
        self.channel.close()
        self.channel.unassign()


class temperatureCallback(event.EventCallback):
    def __init__(self):
        self.temperature = 0

    def process(self, msg, *args):
        print args
        print args

        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print msg.payload
            if ord(msg.payload[0]) == 1:
                tempTemperature = struct.unpack('<h', "".join(msg.payload[-2:]))[0] * 0.01
                if tempTemperature != 0:
                    self.temperature = tempTemperature

    def start(self, antnode, network):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:TEM'
        self.channel.assign(network, CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(25, 0, 0)
        self.channel.searchTimeout = TIMEOUT_NEVER
        self.channel.period = 8192
        self.channel.frequency = 57
        self.channel.open()
        self.channel.registerCallback(self)

    def stop(self):
        self.channel.close()
        self.channel.unassign()


class cadenceCallback(event.EventCallback):
    def __init__(self, circ=2.136):
        '''
        to calculate speed from RPM give the circumference of the wheel.
        '''
        self.cadence = 0.
        self.pedalRevolutions = 0.
        self.wheelRevolutions = 0.
        self.wheelRPM = 0.
        self.wheelRPS = 0.
        self.speed = 0.
        self.lastPedalTime = 0.
        self.lastWheelTime = 0.
        self.wheelCircumference = circ
        self.pedalEventTime = 0.
        self.wheelEventTime = 0.

    def start(self, antnode, network):
        self.channel = antnode.getFreeChannel()
        self.channel.name = 'C:CDM'
        self.channel.assign(network, CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(121, 0, 0)
        self.channel.searchTimeout = TIMEOUT_NEVER
        self.channel.period = 8086
        self.channel.frequency = 57
        self.channel.open()
        self.channel.registerCallback(self)

    def stop(self):
        self.channel.close()
        self.channel.unassign()

    def process(self, msg, *args):
        print msg
        print args
        print type(msg.payload)
        print len(msg.payload)
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            (pedalTime, pedalRevolutions, wheelTime, wheelRevolutions) = numpy.array(
                numpy.frombuffer(msg.payload[-8:], dtype=numpy.uint16), dtype="float")
            pedalTime /= 1024.
            wheelTime /= 1024.
            if wheelTime < self.lastWheelTime:
                self.lastWheelTime -= 64.
            if pedalTime < self.lastPedalTime:
                self.lastPedalTime -= 64.
            if wheelRevolutions < self.wheelRevolutions:
                self.wheelRevolutions -= 65536.
            if pedalRevolutions < self.pedalRevolutions:
                self.pedalRevolutions -= 65536.
            if self.lastPedalTime < pedalTime:
                self.cadence = (pedalRevolutions - self.pedalRevolutions) / (pedalTime - self.lastPedalTime) * 60
                self.lastPedalTime = pedalTime
                self.pedalRevolutions = pedalRevolutions
                self.pedalEventTime = time.time()
            if self.lastWheelTime < wheelTime:
                self.wheelRPS = (wheelRevolutions - self.wheelRevolutions) / (wheelTime - self.lastWheelTime)
                self.lastWheelTime = wheelTime
                self.wheelRevolutions = wheelRevolutions
                self.wheelRPM = self.wheelRPS * 60
                self.speed = self.wheelRPS * self.wheelCircumference * 3600.
                self.wheelEventTime = time.time()
            if self.wheelEventTime + 3 < time.time():
                self.wheelRPS = 0.
                self.wheelRPM = 0.
                self.speed = 0.
            if self.pedalEventTime + 3 < time.time():
                self.cadence = 0.


class antDevices():
    def __init__(self):
        self.stick = driver.USB2Driver(idProduct=0x1008)
        self.antnode = Node(self.stick)
        self.antnode.start()
        self.network = Network(key=NETWORK_KEY_ANT_PLUS, name='N:ANT+')
        self.antnode.setNetworkKey(NETWORK_NUMBER_PUBLIC, self.network)
        self.devices = []

    def add_device(self, device):
        device.start(self.antnode, self.network)
        self.devices.append(device)

    def stop(self):
        for device in self.devices:
            device.stop()
        self.antnode.stop()

    def __exit__(self):
        self.stop()


class antSensors():
    def __init__(self):
        self.myMonitors = antDevices()
        self.HRM = heartRateCallback()
        self.myMonitors.add_device(self.HRM)
        self.TEM = temperatureCallback()
        self.myMonitors.add_device(self.TEM)
        self.CDM = cadenceCallback()
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


if __name__ == '__main__':
    test = antSensors()
    for i in range(200):
        try:
            print test.heartRate,
            print test.cadence,
            print test.wheelRPM,
            print test.temperature
            time.sleep(.1)
        except KeyboardInterrupt:
            test.stopController()
            test.join()
            break
