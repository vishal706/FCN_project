import socket, optparse
import netifaces as ni
import Packet as Packet
import codecs
# creates an RUDP connection

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
                
    def sendData(self, filelocation):
        self.f = open(filelocation, 'rb')
        data = self.f.read(100)
        self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
        self.packetIndex += 1
        while True:
            self.s.sendto(self.packetIndex-1, (self.dstIP, self.dstPort) )
            data = self.f.read(100)
            self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
            self.packetIndex += 1
            if not data:
                self.f.close()
                self.deleteConnection()
                break

    def deleteConnection(self):
        self.s.close()
