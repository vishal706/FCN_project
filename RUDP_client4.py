import socket, optparse
import netifaces as ni
from Packet import Packet 
import select
import codecs
import pickle
import time

class RUDP_client4():
    '''Multiplicative Increase and Multiplicative decrease factor of 2.
    basically on NACK window increases but on ECN window decreases
    IF a packet is lost, the sliding windows restarts from the lost packet'''
    def __init__(self, logger, srcIP, dstIP, srcPort, dstPort, segmentSize, initialWindowSize, maxWindowSize):
        self.logger = logger
        self.logger.info("Initialising :: " + self.__class__.__name__)
        self.srcIP = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.initialWindowSize = initialWindowSize
        self.maxWindowSize = maxWindowSize
        self.segmentSize = int(segmentSize)
        self.transmitCount = 0
        self.timeoutCounter = 0
        self.maxTimeout = 50
        self.sequenceMapping = {}
        self.packetIndex = -1
        self.sequenceNo = 0
        self.cw = self.initialWindowSize
        self.createConnection()

    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(0.5) #setting timeout fro recv n socket
        
        intialMessage = "Hi"
        self.s.sendto(intialMessage.encode(), (self.dstIP, self.dstPort) )
        time.sleep(2)
        if self.waitACK(-1):
            time.sleep(2)
            # self.s.sendto(intialMessage.encode(), (self.dstIP, self.dstPort) )
            self.logger.info("Connection Established from server")
        return
                
    def sendData(self, filelocation):
        # self.logger.info("hello")
        self.f = open(filelocation, 'rb')
        data = self.f.read(self.segmentSize)
        while data:
            self.packetIndex += 1
            self.sequenceMapping[self.packetIndex] = pickle.dumps(Packet(self.packetIndex, data))
            data = self.f.read(self.segmentSize)
        self.logger.info("Total segments :: " + str(self.packetIndex + 1))
        self.sendWindow()
        return (self.transmitCount - self.packetIndex)
        
        
    def sendWindow(self):
        while True:
            w=self.cw
            i=0
            while i<w:
                self.s.sendto(self.sequenceMapping[self.sequenceNo + i], (self.dstIP, self.dstPort) )
                # time.sleep(0.5)
                i+=1
                if (self.sequenceNo + i) > self.packetIndex:
                    break
            self.transmitCount += i
            next = self.waitNACK()

            if next >= self.packetIndex:#end
                return
            elif next == -1:
                self.logger.info("Different response received")
                return
                # self.sequenceNo = self.sequenceNo + w
            elif next != -2:
                self.sequenceNo = next
            self.logger.info(str(self.sequenceNo) + ":"  + str(self.cw))
            # break
        # self.sendWindow()
    
    def sendPacket(self, next):
        self.s.sendto(self.sequenceMapping[next], (self.dstIP, self.dstPort) )
        while not self.waitACK(next):
            self.s.sendto(self.sequenceMapping[next], (self.dstIP, self.dstPort) )
    
    def waitACK(self, sequenceNo):
        try:
            data, addr = self.s.recvfrom(100)
            data = data.decode()
            resp = data.split(":")
            self.logger.info(str(resp[1]) + ":" + data)
            if(resp[0]=="ACK" and int(resp[1]) == sequenceNo):
                return True
        except Exception as e:
            self.timeoutCounter += 1
            if self.timeoutCounter > self.maxTimeout:
                self.timeoutCounter = 0
                self.logger.info(e)
            return False

    def waitNACK(self):
        try:
            data, addr = self.s.recvfrom(100)
            data = data.decode()
            resp = data.split(":")
            self.logger.info("waitNACK-" + str(resp))
            resp[1]=int(resp[1])
            # self.timeoutCounter = 0
            if(resp[0]=="ECN"):
                #Decrease window since congestion detected
                # k=resp[1]-1
                # while k in self.sequenceMapping:
                #     del self.sequenceMapping[k]
                    # k-=1
                self.cw = max(self.initialWindowSize, int((self.cw)/2))
            else:
                #Increase window since no congestion detected
                self.cw = min(self.maxWindowSize, int((self.cw)*2))
            return resp[1]
            
        except Exception as e:
            # self.logger.info(e)
            return -2

    def deleteConnection(self):
        self.s.close()
