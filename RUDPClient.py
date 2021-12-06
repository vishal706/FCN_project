import optparse
from timeit import default_timer as timer
import logging
import os

from RUDP_client1 import RUDP_client1
from RUDP_client_NACK import RUDP_client_NACK
from RUDP_client_minimal import RUDP_client_minimal
from RUDP_client_MIMD_RTT_calculation import RUDP_client_MIMD_RTT_calculation
from RUDP_client3 import RUDP_client3
from RUDP_client2 import RUDP_client2
from RUDP_client4 import RUDP_client4

# python3 RUDPClient.py -i "10.0.0.2" -p "101" -f "send_10000.b" --fT "0.25" --priority "1"
parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=100)
parser.add_option('-f', dest='srcFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=50000)
parser.add_option('--fT', dest='feedbackTime', type='float', default=0.25)
parser.add_option('--priority', dest='priority', type='int', default=100)
# parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()

log_location = "./log_files/client_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + str(options.priority) + "__" + ".log"

os.makedirs(os.path.dirname(log_location), exist_ok=True)
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=log_location, mode='a')
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
      Rudp = RUDP_client1(logger, '127.0.0.1', options.dstIP, options.port, options.port,\
           options.segmentSize, options.initialWindowSize, options.maxWindowSize)
elif options.priority == 2:
      Rudp = RUDP_client2(logger, '127.0.0.1', options.dstIP, options.port, options.port,\
            options.segmentSize, options.initialWindowSize, options.maxWindowSize)
elif options.priority == 3:
      Rudp = RUDP_client3(logger, '127.0.0.1', options.dstIP, options.port, options.port,\
           options.segmentSize, options.initialWindowSize, options.maxWindowSize)
elif options.priority == 4:
      Rudp = RUDP_client4(logger, '127.0.0.1', options.dstIP, options.port,\
             options.port, options.segmentSize)
else:
      print("please enter priority")
      exit()

start = timer()
Rudp.createConnection()
logger.info("Connection established")
file_name = "./send_files/" + options.srcFile
retransmission = Rudp.sendData(file_name)
logger.info("Retransmission count = " + str(retransmission))
end = timer()

logger.info("Sending complete in time:: " + str(end - start))