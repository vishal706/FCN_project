import optparse
from timeit import default_timer as timer

import logging
import os

import matplotlib.pyplot as plt

# python3 RUDP_testing_client.py -i "10.0.0.2" b "50000" -p "100" -s "1000" -f "send_10000.b" --icw "1024" --mcw "50000" --fT "0.25"

parser = optparse.OptionParser()
parser.add_option('-i', dest='dstIP', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-s', dest='segmentSize', type='int', default=100)
parser.add_option('-f', dest='srcFile', default="README.md")
parser.add_option('-b', dest='bufferSize', type='int', default=50000)
parser.add_option('--icw', dest='initialWindowSize', type='int', default=1024)
parser.add_option('--mcw', dest='maxWindowSize', type='int', default=5000)
parser.add_option('--fT', dest='feedbackTime', type='float', default=0.25)
# parser.add_option('--priority', dest='priority', type='int', default=100)
# parser.add_option('-m', dest='msg')

(options, args) = parser.parse_args()


timer_1 = [2]
timer_2 = [2]
timer_3 = [4]


for i in range(5):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPClient.py -i "{options.dstIP}" -p "{options.port + 1}" -f "{options.srcFile}" \
--fT "{options.feedbackTime}" --icw "{options.initialWindowSize}" \
--mcw "{options.maxWindowSize}" -s "{options.segmentSize}" --priority "1"'
    print(command)
    os.system(command)
    end = timer()
    timer_1.append(end - start)

for i in range(5):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPClient.py -i "{options.dstIP}" -p "{options.port + 2}" -f "{options.srcFile}" \
--fT "{options.feedbackTime}" --icw "{options.initialWindowSize}" \
--mcw "{options.maxWindowSize}" -s "{options.segmentSize}" --priority "2"'
    print(command)
    os.system(command)
    end = timer()
    timer_2.append(end - start)


for i in range(5):
    start = timer()
    ### command goes here.
    command = f'python3 RUDPClient.py -i "{options.dstIP}" -p "{options.port + 3}" -f "{options.srcFile}" \
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
textstr = '\n'.join((
    f'segmentSize = {options.segmentSize}',
    f'initialWindowSize = {options.initialWindowSize}',
    f'maxWindowSize = {options.maxWindowSize}',
    f'feedbackTime = {options.feedbackTime}',
    f'bufferSize = {options.bufferSize}'))

# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# plt.text(0.05, 0.95, textstr, fontsize=14,
#         verticalalignment='top')

# plt.figtext(-0.05, 3.5, s=textstr, horizontalalignment = "center")
plt.text(-0.05, 3.5, textstr)

file_name = "/home/mininet/FCN_project/graphs/client_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + str(options.bufferSize) + "__" + ".png"
plt.savefig(file_name)
plt.show()
