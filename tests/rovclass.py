from rovcontroller import  ROVControl, getDefaultPackets
import unittest

ROVIP = "localhost"
CMDPORT = 1944

class CanDevice(object):
    def __init__(self, name, conconfig=""):
        if type(name) != str:
            raise TypeError("Name needs to be a string")
        self.name = name

    def connect(self):
        # Connect the can device
        pass

    def disconnect(self):
        # disconnect the can device
        pass

class RovInterface(object):
    def __init__(self, ip, port, devices=[], neton = True):
        if neton:
            self._netInter = ROVControl(ip, port)
        else:
            self._netInter = None


        if any([type(d) != CanDevice for d in devices]):
            raise TypeError("list is not can devices")

        self._devices = {d.name: d for d in devices}
    
    @property
    def dev(self):
        return self._devices

    @property
    def lsdev(self):
        return self._devices.iterkeys()

    def sendPacket(self,packet):
        if self._netInter != None:
            self._netInter.getFlask(packet)


    def readPacket(self):
        if self._netInter != None:
            return self._devices.getClient()
        else:
            return {}

    def killRov(self):
        #kill the rov
        for d in self._devices.itervalues():
            d.disconnect()

class RovTest(unittest.TestCase):
    def setUp(self):
        d1 = CanDevice("d1")
        d2 = CanDevice("d2")
        d3 = CanDevice("d3")
        self.rovI = RovInterface(ROVIP,CMDPORT,[d1,d2,d3],neton=False)

    def tearDown(self):
        self.rovI.killRov()