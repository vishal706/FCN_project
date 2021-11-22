import socket, optparse

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

f = open('send.txt','r')
data = f.read(100)
i=0
while True:
    print(data)
    s.sendto(data, (options.ip, options.port) )
    data = f.read(100)
    if not data:
        f.close()
        s.close()
        break