import unittest

ROVIP = "localhost"
ROVPORT = 5000

class CanDevice(object):
    def __init__(self,name,canConfFile=""):
        if type(name) != str:
            raise TypeError("Name needs to be a string you idiot")
        self.name = name

    def connect(self):
        pass

    def disconnect(self):
        pass

    def destroyDevice(self):
        pass

class ROVInterface(object):
    def __init__(self,rovip,port,devices = []):
       self.sockInt = None #ROVControl(rovip,port)
       if any([type(d) != CanDevice for d in devices]):
          raise TypeError("Devices need to be CAN devices")
       self._devices = {d.name:d for d in devices}
       for d in self._devices.itervalues():
           d.connect()
        
    def sendPacket(self,packet):
        self.sockInt.getFlask(packet)

    def recvPacket(self):
        return self.sockInt.getClient()

    @property
    def dev(self):
        return self._devices

    @property
    def lsdev(self):
        return list(self._devices.iterkeys())

    def killrov(self):
        pass

class ROVTest(unittest.TestCase):
    def setUp(self):
        # Turn on the rov

        # Connect peripherals to the ROV
        d1 = CanDevice("d1")
        d2 = CanDevice("d2")
        d3 = CanDevice("d3")
        self.rovI = ROVInterface(ROVIP,ROVPORT,[d1,d2,d3])

    def tearDown(self):
        # Turn off rov
        self.rovI.killrov()