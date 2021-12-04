# server.py

import socket                   # Import socket module
import optparse
from timeit import default_timer as timer

parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-s', dest='segmentSize', type='int', default=1000)
parser.add_option('-p', dest='dstPort', type='int', default=12345)
parser.add_option('-f', dest='dstFile', default="received_data")


parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

# Reserve a port for your service.
# to run ::  python3 TCPServer.py -i 10.0.0.2 -f "1.5MB.mp4"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# Create a socket object
# host = socket.gethostname()     # Get local machine name
print(options.dstIP, int(options.dstPort))
s.bind((options.dstIP, int(options.dstPort)))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')
start = timer()
while True:
   conn, addr = s.accept()     # Establish connection with client.
   print('Got connection from' +str(addr))
   data = conn.recv(options.segmentSize)
   print('Server received', repr(data))
   
   # f='send.txt'#'1.5MB.mp4'
   f = open(options.dstFile,'rb')
   l = f.read(options.segmentSize)
   while (l):
      conn.send(l)
   #    print('Sent ',repr(l))
      l = f.read(options.segmentSize)
   f.close()
   end = timer()
   print('Done sending in time::' + str(end - start))
   # conn.send(b'Thank you for connecting')
   conn.close()

