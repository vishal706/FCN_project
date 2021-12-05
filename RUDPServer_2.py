import optparse
from Packet import Packet
from timeit import default_timer as timer
from RUDP_server2 import RUDP_server2

parser = optparse.OptionParser()

#  python3 RUDPServer_2.py -i "10.0.0.2" -p 107 -f "recv.txt"
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', default=100)
parser.add_option('-b', dest='bufferSize', type='int', default=50000)
parser.add_option('-f', dest='dstFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=50000)


(options, args) = parser.parse_args()

Rudp_2 = RUDP_server2(options.port, options.segmentSize, options.bufferSize)

start = timer()
Rudp_2.createConnection()
file_location = "./received_files/" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.maxWindowSize) + "_" + options.dstFile
print("Connection established")
Rudp_2.ReceiveData(file_location)
end = timer()

print("Sending complete in time:: " + str(end - start))