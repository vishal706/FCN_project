import socket, optparse
import netifaces as ni
from Packet import Packet 
import codecs
import pickle

class RUDP():

    def __init__(self, srcIP, dstIP, srcPort, dstPort, segmentSize):
        self.srcIP = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.segmentSize = int(segmentSize)
        self.createConnection()
        self.sequenceMapping = {}
        self.packetIndex = 0

    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(2.0)
                
    def sendData(self, filelocation):
        self.f = open(filelocation, 'rb')
        data = self.f.read(100)
        self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
        self.packetIndex += 1
        pickleData = pickle.dumps(self.sequenceMapping[self.packetIndex-1])
        while True:
            self.s.sendto(pickleData, (self.dstIP, self.dstPort) )
            while( not self.waitACK(self.packetIndex-1)):
                self.s.sendto(pickleData, (self.dstIP, self.dstPort) )
            self.waitACK(self.packetIndex-1)
            data = self.f.read(100)
            if not data:
                self.f.close()
                self.deleteConnection()
                break
            self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
            self.packetIndex += 1
            pickleData = pickle.dumps(self.sequenceMapping[self.packetIndex-1])

    def waitACK(self, sequenceNo):
        try:
            data, addr = self.s.recvfrom(512)
            print(str(sequenceNo) + ":" + data)
            return True
        except Exception as e:
            print(e)
            return False

    def deleteConnection(self):
        self.s.close()
