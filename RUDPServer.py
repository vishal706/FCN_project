import optparse
from Packet import Packet 
from timeit import default_timer as timer
import logging
import os
#Create and configure logger

# from RUDP_server_MIMD import RUDP_server_MIMD
from RUDP_server_minimal import RUDP_server_minimal
from RUDP_server3 import RUDP_server3
from RUDP_server2 import RUDP_server2
parser = optparse.OptionParser()

#  python3 RUDPServer.py -i "10.0.0.2" -p 101 -f "recv.txt" 
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', default=100)
parser.add_option('-b', dest='bufferSize', type='int', default=50000)
parser.add_option('-f', dest='dstFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=50000)


(options, args) = parser.parse_args()


file_location = "./received_files/" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.maxWindowSize) + "_" + options.dstFile

log_location = "./log_files/server_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.maxWindowSize) + "_" +".log"


os.makedirs(os.path.dirname(log_location), exist_ok=True)
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=log_location, mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)


consoleHandler = logging.StreamHandler()
consoleFormatter = logging.Formatter('%(message)s')
consoleHandler.setFormatter(consoleFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


# Rudp = RUDP_server3(logger, options.port, options.segmentSize, options.bufferSize)
# Rudp = RUDP_server2(logger, options.port, options.segmentSize, options.bufferSize)
Rudp = RUDP_server_minimal(logger, options.port, options.segmentSize, options.bufferSize)

start = timer()
Rudp.createConnection()
logger.info("Connection established")
Rudp.ReceiveData(file_location)
end = timer()

logger.info("Sending complete in time:: " + str(end - start))