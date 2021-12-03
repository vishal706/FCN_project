import optparse
from timeit import default_timer as timer

from RUDP_GoBackN import RUDP_GoBackN 

parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-s', dest='segmentSize', default=1000)
parser.add_option('-p', dest='dstPort', type='int', default=12345)
parser.add_option('-f', dest='srcFile', default="README.md")
parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()

Rudp = RUDP_GoBackN('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.segmentSize)

start = timer()
Rudp.createConnection()
Rudp.sendData(options.srcFile)
end = timer()

print("Sending complete in time:: " + str(end - start))