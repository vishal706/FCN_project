import socket, optparse
import netifaces as ni
from Packet import Packet 
import select
import codecs
import pickle
import time

class RUDP_GoBackN():

    def __init__(self, srcIP, dstIP, srcPort, dstPort, segmentSize):
        self.srcIP = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.segmentSize = int(segmentSize)
        self.createConnection()
        self.sequenceMapping = {}
        self.packetIndex = -1
        self.sequenceNo = 0
        self.cw = 5

    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(2.0) #setting timeout fro recv n socket
        # intialMessage = "Hi"
        # self.s.sendto(intialMessage.encode(), (self.dstIP, self.dstPort) )
        # while not self.waitACK(-1):
        #     self.s.sendto(intialMessage.encode(), (self.dstIP, self.dstPort) )
        # print("Connection Established from client")
                
    def sendData(self, filelocation):
        print("hello")
        self.f = open(filelocation, 'rb')
        data = self.f.read(self.segmentSize)
        while data:
            self.packetIndex += 1
            self.sequenceMapping[self.packetIndex] = pickle.dumps(Packet(self.packetIndex, data))
            data = self.f.read(self.segmentSize)
        print("Total segments :: " + str(self.packetIndex + 1))
        self.sendWindow()
        
        
    def sendWindow(self):
        w=self.cw
        i=0
        while i<w:
            self.s.sendto(self.sequenceMapping[self.sequenceNo + i], (self.dstIP, self.dstPort) )
            # time.sleep(0.5)
            i+=1
            if (self.sequenceNo + i) > self.packetIndex:
                break
        next = self.waitNACK()

        if next >= self.packetIndex:#end
            return
        elif next == -1:
            self.sequenceNo = self.sequenceNo + w
        elif next != -2:
            self.sequenceNo = next

        self.sendWindow()
    
    def sendPacket(self, next):
        self.s.sendto(self.sequenceMapping[next], (self.dstIP, self.dstPort) )
        while not self.waitACK(next):
            self.sendPacket(next)
    
    def waitACK(self, sequenceNo):
        try:
            data, addr = self.s.recvfrom(100)
            data = data.decode()
            resp = data.split(":")
            print(str(resp[1]) + ":" + data)
            if(resp[0]=="ACK" and int(resp[1]) == sequenceNo):
                return True
        except Exception as e:
            print(e)
            return False

    def waitNACK(self):
        try:
            data, addr = self.s.recvfrom(100)
            data = data.decode()
            resp = data.split(":")
            # print("waitNACK-" + str(resp))
            resp[1]=int(resp[1])
            if(resp[0]=="ECN"):
                self.cw = (self.cw)
                return resp[1]
            else:
                return -1
        except Exception as e:
            print(e)
            return -2

    def deleteConnection(self):
        self.s.close()
