import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle

# python myclient.py -i 10.0.0.2 -s 100
# python myServer.py -i 10.0.0.1
# ReceivedPacket = set()
buffer = {}
nextSequenceNo = 0
parser = optparse.OptionParser()
selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=50)
parser.add_option('-w', dest='bufferSize', type='int', default=5)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind( (selfip, options.port) )

f = open(selfip + '_recv.txt', 'wb+')
while True:
    data, addr = s.recvfrom(options.segmentSize + 100)
    packet = pickle.loads(data)
    result = "-".join(str(key) for key, value in buffer.items())
    print(result)
    if(len(buffer) >= options.bufferSize):
        #drop packets
        print("Exceeded buffer")
        if packet.sequenceNo == nextSequenceNo:
            f.write(b"%s" % packet.payload)
            nextSequenceNo += 1
        else:
            nack = "NACK:" + str(packet.sequenceNo)
            s.sendto(nack.encode(), (addr[0], addr[1]) )
    else:
        ack = "ACK:" + str(packet.sequenceNo)
        s.sendto(ack.encode(), (addr[0], addr[1]) )
        if packet.sequenceNo >=  nextSequenceNo:
            buffer[packet.sequenceNo] = packet.payload
        while nextSequenceNo in buffer:
            f.write(b"%s" % buffer[nextSequenceNo])
            del buffer[nextSequenceNo]
            nextSequenceNo += 1
        f.flush()