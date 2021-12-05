import optparse
from timeit import default_timer as timer

from RUDP_client_MIMD import RUDP_client_MIMD
from RUDP_client_minimal import RUDP_client_minimal
from RUDP_client_MIMD_RTT_calculation import RUDP_client_MIMD_RTT_calculation
from RUDP_client3 import RUDP_client3
from RUDP_client2 import RUDP_client2
import matplotlib.pyplot as plt

# python3 RUDPClient_testing.py -i 10.0.0.2  -p 105 -f "send.txt"
parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='dstPort', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', default=100)
parser.add_option('-f', dest='srcFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=50000)
parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()

# timer_minimal = []
timer_MIMD = []
timer_2 = []
timer_3 = []

# for i in range(5):
#     Rudp = RUDP_client_minimal('127.0.0.1', options.dstIP, options.dstPort, options.dstPort, options.segmentSize)
#     start = timer()
#     Rudp.createConnection()
#     print("Connection established")
#     file_name = "./send_files/" + options.srcFile
#     Rudp.sendData(file_name)
#     end = timer()
#     timer_minimal.append(end - start)

# for i in range(5):
#     Rudp = RUDP_client_MIMD('127.0.0.1', options.dstIP, options.dstPort + 1, options.dstPort + 1, options.segmentSize,
#                             options.initialWindowSize, options.maxWindowSize)
#     start = timer()
#     Rudp.createConnection()
#     print("Connection established")
#     file_name = "./send_files/" + options.srcFile
#     Rudp.sendData(file_name)
#     end = timer()
#     timer_MIMD.append(end - start)

for i in range(10):
    Rudp = RUDP_client2('127.0.0.1', options.dstIP, options.dstPort + 2, options.dstPort + 2, options.segmentSize,
                        options.initialWindowSize, options.maxWindowSize)
    start = timer()
    Rudp.createConnection()
    print("Connection established")
    file_name = "./send_files/" + options.srcFile
    Rudp.sendData(file_name)
    end = timer()
    timer_2.append(end - start)

for i in range(10):
    Rudp = RUDP_client3('127.0.0.1', options.dstIP, options.dstPort + 3, options.dstPort + 3, options.segmentSize,
                        options.initialWindowSize, options.maxWindowSize)
    start = timer()
    Rudp.createConnection()
    print("Connection established")
    file_name = "./send_files/" + options.srcFile
    Rudp.sendData(file_name)
    end = timer()
    timer_3.append(end - start)

# print(f"timer minimal: {timer_minimal}")

plt.plot(timer_MIMD)
plt.plot(timer_2)
plt.plot(timer_3)
plt.legend(["MIMD", "2", "3"])

plt.title('Total time taken to transfer whole data')
plt.xlabel('Iterations')
plt.ylabel('Time')
plt.show()

# print(f"timer MIMD: {timer_MIMD}")
# print(f"timer 2: {timer_2}")
# print(f"timer 3: {timer_3}")
