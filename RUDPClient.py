import optparse
from timeit import default_timer as timer

from RUDP_client_MIMD import RUDP_client_MIMD
from RUDP_client_minimal import RUDP_client_minimal
from RUDP_client_MIMD_RTT_calculation import RUDP_client_MIMD_RTT_calculation

# python3 RUDPClient.py -i 10.0.0.2 -f "send.txt" -p 101
parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-s', dest='segmentSize', default=100)
parser.add_option('-p', dest='dstPort', type='int', default=12345)
parser.add_option('-f', dest='srcFile', default="README.md")
parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()

# Rudp = RUDP_client_MIMD('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.segmentSize)
# Rudp = RUDP_client_minimal('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.segmentSize)
Rudp = RUDP_client_MIMD_RTT_calculation('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.segmentSize)

start = timer()
Rudp.createConnection()
file_name = "./send_files/" + options.srcFile
Rudp.sendData(file_name)
end = timer()

print("Sending complete in time:: " + str(end - start))