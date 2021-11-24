import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle

# python myclient.py -i 10.0.0.2 -s 100
# python myServer.py -i 10.0.0.1
ReceivedPacket = set()
parser = optparse.OptionParser()
selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
# parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind( (selfip, options.port) )

f = open(selfip + '_recv.txt', 'wb+')
while True:
    data, addr = s.recvfrom(512)
    packet = pickle.loads(data)
    s.sendto(str(packet.sequenceNo) + ":ACK", (addr[0], addr[1]) )
    if packet.sequenceNo not in ReceivedPacket:
        print("%s " % packet.payload)
        f.write("%s" % packet.payload)
        ReceivedPacket.add(packet.sequenceNo)
    # print(addr)
    # print(str(packet.sequenceNo) + ":" + addr[0])
    # f.flush()