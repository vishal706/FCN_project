import socket, optparse
import netifaces as ni
from Packet import Packet 
import select
import codecs
import pickle
import time

class RUDP_client_minimal():

    def __init__(self, srcIP, dstIP, srcPort, dstPort, segmentSize):
        print("Initialising :: " + self.__class__.__name__)
        self.srcIP = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.segmentSize = int(segmentSize)
        # self.createConnection()
        self.sequenceMapping = {}
        self.packetIndex = -1

    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(2.0) #setting timeout fro recv n socket
                
    def sendData(self, filelocation):
        self.f = open(filelocation, 'rb')
        data = self.f.read(self.segmentSize)
        self.packetIndex += 1
        # self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
        # pickleData = pickle.dumps(self.sequenceMapping[self.packetIndex])
        self.sequenceMapping[self.packetIndex] = pickle.dumps(Packet(self.packetIndex, data))
        while True:
            self.s.sendto(self.sequenceMapping[self.packetIndex], (self.dstIP, self.dstPort) )
            while( not self.waitACK(self.packetIndex)):
                self.s.sendto(self.sequenceMapping[self.packetIndex], (self.dstIP, self.dstPort) )
            data = self.f.read(self.segmentSize)
            if not data:
                self.f.close()
                self.deleteConnection()
                break
            del self.sequenceMapping[self.packetIndex]
            self.packetIndex += 1
            # self.sequenceMapping[self.packetIndex] = Packet(self.packetIndex, data)
            # pickleData = pickle.dumps(self.sequenceMapping[self.packetIndex])
            self.sequenceMapping[self.packetIndex] = pickle.dumps(Packet(self.packetIndex, data))

    def waitACK(self, sequenceNo):
        try:
            data, addr = self.s.recvfrom(100)
            data = data.decode()
            print(str(sequenceNo) + ":" + data)
            resp = data.split(":")
            if(resp[0]=="ACK") and int(resp[1]) == sequenceNo:
                return True
            # if(resp[0]=="NACK"):
            #     sequenceNoNack = resp[1]
            #     while( not self.waitACK(sequenceNoNack)):
            #         self.s.sendto(self.sequenceMapping[sequenceNoNack], (self.dstIP, self.dstPort) )
        except Exception as e:
            print(e)
            return False

    def deleteConnection(self):
        self.s.close()