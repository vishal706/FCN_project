
# client.py

import socket                   # Import socket module
import optparse
from timeit import default_timer as timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#python3 TCPClient.py -i 10.0.0.2 -f "recv.mp4"
parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-s', dest='segmentSize', type='int', default=1000)
parser.add_option('-p', dest='dstPort', type='int', default=12345)
parser.add_option('-f', dest='srcFile', default="README.md")

parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

start = timer()

print(options.dstIP, int(options.dstPort))
s.connect((options.dstIP, int(options.dstPort)))
s.send(b"Hello server!")

with open(("TCP_" + options.srcFile), 'wb') as f:
    print('file opened')
    while True:
        print("Received")
        data = s.recv(options.segmentSize)
        if not data:
            break
        f.write(data)

f.close()
end = timer()
print('Successfully get the file in time ::' + str(end - start))
s.close()
print('connection closed')