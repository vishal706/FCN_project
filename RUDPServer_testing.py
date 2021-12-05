import optparse
from Packet import Packet
from timeit import default_timer as timer
import logging
import os
#Create and configure logger
from RUDP_server1 import RUDP_server1
from RUDP_server_minimal import RUDP_server_minimal
from RUDP_server_MIMD_RTT_calculation import RUDP_server_MIMD_RTT_calculation

from RUDP_server_minimal import RUDP_server_minimal
from RUDP_server3 import RUDP_server3
from RUDP_server2 import RUDP_server2

parser = optparse.OptionParser()

#  python3 RUDPServer_testing.py -i "10.0.0.2" -p "105" -f "recv.txt" --fT "0.25" -t 1
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=105)
parser.add_option('-s', dest='segmentSize', default=100)
parser.add_option('-b', dest='bufferSize', type='int', default=50000)
parser.add_option('-f', dest='dstFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=50000)
parser.add_option('--fT', dest='feedbackTime', type='float', default=0.25)
parser.add_option('-t', dest='serverType', type='int', default=1)


(options, args) = parser.parse_args()


file_location = "./received_files/" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + options.dstFile

log_location = "./log_files/server_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" +".log"


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

if options.serverType == 1:
    Rudp = RUDP_server1(logger, options.port+1, options.segmentSize, options.bufferSize, options.feedbackTime)
elif options.serverType == 2:
    Rudp = RUDP_server2(logger, options.port+2, options.segmentSize, options.bufferSize, options.feedbackTime)
elif options.serverType == 3:
    Rudp = RUDP_server3(logger, options.port+3, options.segmentSize, options.bufferSize, options.feedbackTime)
else:
    Rudp = RUDP_server_minimal(logger, options.port, options.segmentSize, options.bufferSize, options.feedbackTime)

start = timer()
Rudp.createConnection()
logger.info("Connection established")
Rudp.ReceiveData(file_location)
end = timer()

logger.info("Sending complete in time:: " + str(end - start))