import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle
import threading


class RUDP_server_NACK():
    def __init__(self, port, segmentSize, bufferSize):
        self.buffer = {}
        self.nextSequenceNo = 0
        self.port = port
        self.segmentSize = segmentSize
        self.s = None
        self.selfip = None
        self.bufferSize = bufferSize
    
    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.s.settimeout(1.0)
        self.selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.s.bind( (self.selfip, self.port) )
    
    def _on_timeout(self):
        print("timeout occured")
        self.sendresp("NACK:", self.addr[0], self.addr[1])

    def _start_timer(self):
        # self.OutputLogger("[_start_timer] Starting timer for round {} max_time : self.get_round_timer() {} timestamp {}".format( roundNo,self.get_round_timer(),time.time()))
        self.timer = threading.Timer(0.25, self._on_timeout)
        self.timer.start()

    def _stop_timer(self):
        # self.OutputLogger("[_stop_timer] Entry for round {}".format(roundNo))
        # if roundNo in self.dict_of_timer:
        #     self.OutputLogger(" Stopping timer for roundNo {} timestamp {} ".format( roundNo,time.time()))
        if self.timer is not None:
            self.timer.cancel()

        # self.OutputLogger("[_stop_timer] Exit for round {}".format(roundNo))

    def sendresp(self, respType, sequenceNo, addr_0, addr_1):
        resp = respType + str(sequenceNo)
        # print(resp)
        self.s.sendto(resp.encode(), (addr_0, addr_1) )
    
    def ReceiveData(self, filename):
        f = open(self.selfip + filename, 'wb+')
        while True:
            data, addr = self.s.recvfrom(self.segmentSize + 100)
            packet = pickle.loads(data)
            # ack = "ACK:" + str(packet.sequenceNo)
            self.sendresp("ACK:", packet.sequenceNo, addr[0], addr[1])
            if packet.sequencNo not in self.buffer:
                self.buffer[packet.sequenceNo] = packet.payload
            while self.nextSequenceNo in self.buffer:
                self._stop_timer()
                f.write(b"%s" %self.buffer[self.nextSequenceNo])
                del self.buffer[self.nextSequenceNo]
                self.nextSequenceNo += 1
                self._start_timer()
            f.flush()

