import optparse
from timeit import default_timer as timer


import os

import matplotlib.pyplot as plt

# python3 RUDP_testing_server.py -i "10.0.0.2"  -p "105" -b "5000" -f "send.txt" --icw "1024" --mcw "50000" --fT "0.25"
# python3 RUDPServer.py -i "10.0.0.2" -p "101" -f "recv.txt" --fT "0.25" --priority "1"

parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=100)
parser.add_option('-b', dest='bufferSize', type='int', default=5000)
parser.add_option('-f', dest='dstFile', default="README.md")
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=5000)
parser.add_option('--fT', dest='feedbackTime', type='float', default=0.25)
# parser.add_option('--priority', dest='priority', type='int', default=100)

parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()



timer_1 = []
timer_2 = []
timer_3 = []

for i in range(1):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPServer.py -i "{options.dstIP}" -p "{options.port + 1}" -f "{options.dstFile}" \
--fT "{options.feedbackTime}" --icw "{options.initialWindowSize}" \
--mcw "{options.maxWindowSize}" -s "{options.segmentSize}" --priority "1"'
    print(command)
    os.system(command)
    end = timer()
    timer_1.append(end - start)


for i in range(1):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPServer.py -i "{options.dstIP}" -p "{options.port + 2}" -f "{options.dstFile}" \
--fT "{options.feedbackTime}" --icw "{options.initialWindowSize}" \
--mcw "{options.maxWindowSize}" -s "{options.segmentSize}" --priority "2"'
    print(command)
    os.system(command)
    end = timer()
    timer_2.append(end - start)

for i in range(1):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPServer.py -i "{options.dstIP}" -p "{options.port + 3}" -f "{options.dstFile}" \
--fT "{options.feedbackTime}" --icw "{options.initialWindowSize}" \
--mcw "{options.maxWindowSize}" -s "{options.segmentSize}" --priority "3"'
    print(command)
    os.system(command)
    end = timer()
    timer_3.append(end - start)

plt.plot(timer_1)
plt.plot(timer_2)
plt.plot(timer_3)
plt.legend(["1", "2", "3"])

plt.title('Total time taken to transfer whole data')
plt.xlabel('Iterations')
plt.ylabel('Time')
plt.show()
