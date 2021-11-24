import optparse

from RUDP import RUDP 

parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-s', dest='SegmentSize', default=100)
parser.add_option('-p', dest='dstPort', type='int', default=12345)

parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

Rudp = RUDP('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.SegmentSize)

Rudp.createConnection()
Rudp.sendData('send.txt')