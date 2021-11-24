import socket, optparse
import netifaces as ni

parser = optparse.OptionParser()
selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind( (selfip, options.port) )

f = open(selfip + '_recv.txt', 'wb+')
while True:
    data, addr = s.recvfrom(512)
    f.write("%s" % data)
    # f.write("%s: %s\n" % (addr, data))
    # f.flush()