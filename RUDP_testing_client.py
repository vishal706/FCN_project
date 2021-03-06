import optparse
from timeit import default_timer as timer

import logging
import os

import matplotlib.pyplot as plt

# python3 RUDP_testing_client.py -i "10.0.0.4"  -p "100" -s "100" -b "50000" -f "send_15.b" --icw "1024" --mcw "50000" --fT "0.1"
# python3 RUDPServer.py -i "10.0.0.4" -p "101" -s "100" -b "50000" -f "recv_15.b" --fT "0.1" --priority "1"

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


timer_1 = []
timer_2 = []
timer_3 = []


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

# timer_1 = [7.602732038998511, 5.475548384994909, 6.192044618001091, 6.590054241001781, 5.9031156550045125]
# timer_2 = [8.607846077000431, 10.09384544799832, 7.935086603996751, 7.25913836700056, 7.731159035000019]
# timer_3 = [9.750261357999989, 9.7952436869964, 10.235173731998657, 10.239129595000122, 8.248223855000106]
# timer_1 = [6.743216530994687, 5.977355709997937, 5.3149068060010904, 5.325412235004478, 5.741012362996116]
# timer_2 = [7.36355656899832, 6.8418743680012994, 6.257764028996462, 4.644368727000256, 5.1715113739992375]
# timer_3 = [5.542510102000961, 5.492816213001788, 5.498592156996892, 5.550686763999693, 5.4335575029981555]

print(timer_1)
print(timer_2)
print(timer_3)
plt.plot(timer_1)
plt.plot(timer_2)
plt.plot(timer_3)
plt.legend(["1", "2", "3"])

sfile = options.srcFile.partition('.')
plt.title('Total time taken to transfer whole data')
plt.xlabel('Iterations')
plt.ylabel('Time')
textstr = '\n'.join((
    f'segmentSize = {options.segmentSize}',
    f'initialWindowSize = {options.initialWindowSize}',
    f'maxWindowSize = {options.maxWindowSize}',
    f'feedbackTime = {options.feedbackTime}',
    f'filesize = {sfile[0]}',
    f'bufferSize = {options.bufferSize}'))


y=min(min(timer_1), min(timer_2), min(timer_3))
plt.text(1, y, textstr)



file_name = "/home/mininet/FCN_project/graphs/client_" +  options.dstIP + "_" + str(options.port)\
     + "_" + str(options.initialWindowSize) + "_" + str(options.feedbackTime) +\
           "_" + str(options.maxWindowSize) + "_" + sfile[0] + "_" + str(options.bufferSize) + "_" + ".png"
plt.savefig(file_name)
plt.show()
