import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle



# def waitHandshake(s):
#     global SenderIP
#     global SenderPort
#     data, addr = s.recvfrom(options.segmentSize + 500)
#     print(data)
#     SenderIP = addr[0]
#     SenderPort = addr[1]
#     print("Connection Established from server" + SenderIP + ":" + str(SenderPort))
#     sendresp(s, -1, "ACK:", SenderIP, SenderPort)

class RUDP_server_MIMD():
    def __init__(self, port, segmentSize, bufferSize):
        self.buffer = {}
        self.nextSequenceNo = 0
        self.port = port
        self.segmentSize = segmentSize
        self.s = None
        self.selfip = None
        self.bufferSize = bufferSize
    
    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.s.settimeout(1.0)
        self.selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.s.bind( (self.selfip, self.port) )
    
    
    def sendresp(self, respType, addr_0, addr_1):
        resp = respType + str(self.nextSequenceNo)
        # print(resp)
        self.s.sendto(resp.encode(), (addr_0, addr_1) )
        
    def ReceiveData(self, filename):
        f = open(self.selfip + filename, 'wb+')
        while True:
            try:
                data, addr = self.s.recvfrom(self.segmentSize + 100)
                # print("Received packet:" + data.decode())
                packet = pickle.loads(data)
                # print("buffersize:" + str(len(buffer)) + "-Received:" + str(packet.sequenceNo))
                
                if packet.sequenceNo >  self.nextSequenceNo:
                    if packet.sequenceNo not in self.buffer:
                        self.buffer[packet.sequenceNo] = packet.payload
                    if len(self.buffer)>= self.bufferSize:
                        self.sendresp("ECN:", addr[0], addr[1])
                    else:
                        self.sendresp("NACK1:", addr[0], addr[1])
                elif packet.sequenceNo ==  self.nextSequenceNo:
                    if packet.sequenceNo not in self.buffer:
                        self.buffer[packet.sequenceNo] = packet.payload
                    while self.nextSequenceNo in self.buffer:
                        print("writing " + str(self.nextSequenceNo))
                        f.write(b"%s" % self.buffer[self.nextSequenceNo])
                        del self.buffer[self.nextSequenceNo]
                        self.nextSequenceNo += 1
                    # f.write(b"%s" % packet.payload)
                    # del buffer[nextSequenceNo]
                    f.flush()
                self.sendresp( "NACK2:", addr[0], addr[1])
            except Exception as e:
                # self.sendresp( "NACK:3", addr[0], addr[1])
                print(e)

