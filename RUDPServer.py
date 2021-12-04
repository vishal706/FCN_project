import optparse
from Packet import Packet 
from timeit import default_timer as timer

from RUDP_server_MIMD import RUDP_server_MIMD
from RUDP_server_minimal import RUDP_server_minimal

parser = optparse.OptionParser()

parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=100)
parser.add_option('-w', dest='bufferSize', type='int', default=50000)
parser.add_option('-f', dest='dstFile', default="README.md")


(options, args) = parser.parse_args()


Rudp = RUDP_server_MIMD(options.port, options.segmentSize, options.bufferSize)
# Rudp = RUDP_server_minimal(options.port, options.segmentSize, options.bufferSize)

start = timer()
Rudp.createConnection()
file_location = "./received_files/" +  options.dstIP + "_" + str(options.port) + "_" + options.dstFile
Rudp.ReceiveData(file_location)
end = timer()

print("Sending complete in time:: " + str(end - start))