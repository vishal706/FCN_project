import optparse
from Packet import Packet 
from timeit import default_timer as timer
import logging
import os
#Create and configure logger
from RUDP_server1 import RUDP_server1
from RUDP_server_minimal import RUDP_server_minimal
from RUDP_server_MIMD_RTT_calculation import RUDP_server_MIMD_RTT_calculation
from RUDP_server3 import RUDP_server3
from RUDP_server2 import RUDP_server2
from RUDP_server4 import RUDP_server4

parser = optparse.OptionParser()

# python3 RUDPServer.py -i "10.0.0.2" -p "101" -f "recv_10000.b" --fT "0.25" -s "100" --priority "1"
# python3 RUDP_testing_server.py -i "10.0.0.2"  -p "105" -b "5000" -f "send_10000.b" --icw "1024" --mcw "50000" --fT "0.25"
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=100)
parser.add_option('-b', dest='bufferSize', type='int', default=5000)
parser.add_option('-f', dest='dstFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=5000)
parser.add_option('--fT', dest='feedbackTime', type='float', default=0.25)
parser.add_option('--priority', dest='priority', type='int', default=100)


(options, args) = parser.parse_args()


file_location = "./received_files/" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + str(options.priority) +  "_" + options.dstFile

log_location = "./log_files/server_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + str(options.priority) + "__" + ".log"


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
logger.info(options)
if options.priority == 1:
      Rudp = RUDP_server1(logger, options.port, options.segmentSize, options.bufferSize, options.feedbackTime)
elif options.priority == 2:
      Rudp = RUDP_server2(logger, options.port, options.segmentSize, options.bufferSize, options.feedbackTime)
elif options.priority == 3:
      Rudp = RUDP_server3(logger, options.port, options.segmentSize, options.bufferSize, options.feedbackTime)
elif options.priority == 4:
      Rudp = RUDP_server4(logger, options.port, options.segmentSize, options.bufferSize, options.feedbackTime)
else:
      print("please Enter priority")
      exit()

start = timer()
Rudp.createConnection()
logger.info("Connection established")
Rudp.ReceiveData(file_location)
end = timer()

logger.info("Sending complete in time:: " + str(end - start))