import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle
import time

parser = optparse.OptionParser()
selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=1000)
parser.add_option('-w', dest='bufferSize', type='int', default=5)
(options, args) = parser.parse_args()

SenderIP = "0.0.0.0"
SenderPort = "12345"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind( (selfip, options.port) )
f = open(selfip + '_recv.mp4', 'wb+')


def sendresp(s, nextSequenceNo, respType, addr_0, addr_1):
    resp = respType + str(nextSequenceNo)
    # print(resp)
    s.sendto(resp.encode(), (addr_0, addr_1) )

def waitHandshake(s):
    global SenderIP
    global SenderPort
    data, addr = s.recvfrom(options.segmentSize + 500)
    print(data)
    SenderIP = addr[0]
    SenderPort = addr[1]
    print("Connection Established from server" + SenderIP + ":" + str(SenderPort))
    sendresp(s, -1, "ACK:", SenderIP, SenderPort)



def ReceiveData(s):
    # print("hello")
    buffer = {}
    nextSequenceNo = 0
    while True:
        try:
            data, addr = s.recvfrom(options.segmentSize + 100)
            # print("Received packet:" + data.decode())
            packet = pickle.loads(data)
            # print("buffersize:" + str(len(buffer)) + "-Received:" + str(packet.sequenceNo))
            
            if packet.sequenceNo >  nextSequenceNo:
                if packet.sequenceNo not in buffer:
                    buffer[packet.sequenceNo] = packet.payload
                if len(buffer)>= options.bufferSize:
                    sendresp(s, nextSequenceNo, "ECN:", addr[0], addr[1])
                else:
                    sendresp(s, nextSequenceNo, "NACK:", addr[0], addr[1])
            elif packet.sequenceNo ==  nextSequenceNo:
                if packet.sequenceNo not in buffer:
                    buffer[packet.sequenceNo] = packet.payload
                while nextSequenceNo in buffer:
                    print("writing " + str(nextSequenceNo))
                    f.write(b"%s" % buffer[nextSequenceNo])
                    del buffer[nextSequenceNo]
                    nextSequenceNo += 1
                # f.write(b"%s" % packet.payload)
                # del buffer[nextSequenceNo]
                f.flush()
            sendresp(s, nextSequenceNo, "NACK:", addr[0], addr[1])
        except Exception as e:
            sendresp(s, nextSequenceNo, "NACK:", addr[0], addr[1])
            print(e)


# waitHandshake(s)
ReceiveData(s)