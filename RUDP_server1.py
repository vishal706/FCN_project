import socket, optparse
import netifaces as ni
from Packet import Packet 
import pickle
import threading


class RUDP_server1():
    '''Server/ Receiver sends the NACK feedback reglarly a interval of feedbackTime'''
    def __init__(self, logger, port, segmentSize, bufferSize, feedbackTime):
        self.logger = logger
        logger.info("Initialising :: " + self.__class__.__name__)
        self.buffer = {}
        self.nextSequenceNo = -1
        self.port = port
        self.segmentSize = segmentSize
        self.s = None
        self.selfip = None
        self.bufferSize = bufferSize
        self.addr = None
        self.timer = None
        self.feedbackTime = feedbackTime
    
    def createConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.s.settimeout(1.0)
        self.selfip = ni.ifaddresses(str(ni.interfaces()[-1]))[ni.AF_INET][0]['addr']
        self.s.bind( (self.selfip, self.port) )
        data, self.addr = self.s.recvfrom(self.segmentSize + 100)
        self.logger.info("Received " + str(data) + "from server")
        self.sendresp("ACK:", self.addr[0], self.addr[1])
        self.nextSequenceNo += 1
    
    def _on_timeout(self):
        self.logger.info("timeout occured")
        self.sendresp("NACK3:", self.addr[0], self.addr[1])
        self._start_timer()


    def _start_timer(self):
        # self.OutputLogger("[_start_timer] Starting timer for round {} max_time : self.get_round_timer() {} timestamp {}".format( roundNo,self.get_round_timer(),time.time()))
        self.timer = threading.Timer(self.feedbackTime, self._on_timeout)
        self.timer.start()

    def _stop_timer(self):
        # self.OutputLogger("[_stop_timer] Entry for round {}".format(roundNo))
        # if roundNo in self.dict_of_timer:
        #     self.OutputLogger(" Stopping timer for roundNo {} timestamp {} ".format( roundNo,time.time()))
        if self.timer is not None:
            self.timer.cancel()
        self._start_timer()
        # self.OutputLogger("[_stop_timer] Exit for round {}".format(roundNo))
    
    def sendresp(self, respType, addr_0, addr_1):
        resp = respType + str(self.nextSequenceNo)
        self.s.sendto(resp.encode(), (addr_0, addr_1) )
        
    def ReceiveData(self, filename):
        f = open(filename, 'wb+')
        # self._start_timer()
        while True:
            try:
                data, self.addr = self.s.recvfrom(self.segmentSize + 100)

                packet = pickle.loads(data)
                self.logger.info("buffersize:" + str(len(self.buffer)) + "-Received:" + str(packet.sequenceNo) \
                    + ":nextseq=" + str(self.nextSequenceNo))
                
                if packet.sequenceNo == -1:
                    # exit()
                    self.buffer.clear()
                    self.nextSequenceNo = 0
                    print("yo begin + " + str(self.nextSequenceNo))
                    continue

                if packet.sequenceNo >  self.nextSequenceNo:
                    if packet.sequenceNo not in self.buffer:
                        self.buffer[packet.sequenceNo] = packet.payload
                    if len(self.buffer)>= self.bufferSize:
                        self.sendresp("ECN:", self.addr[0], self.addr[1])
                    # else:
                        # self.sendresp("NACK1:", self.addr[0], self.addr[1])
                elif packet.sequenceNo ==  self.nextSequenceNo:
                    if packet.sequenceNo not in self.buffer:
                        self.buffer[packet.sequenceNo] = packet.payload
                    self._stop_timer()
                    while self.nextSequenceNo in self.buffer:
                        self.logger.info("writing " + str(self.nextSequenceNo))
                        f.write(b"%s" % self.buffer[self.nextSequenceNo])
                        del self.buffer[self.nextSequenceNo]
                        self.nextSequenceNo += 1
                        # f.write(b"%s" % packet.payload)
                        # del buffer[nextSequenceNo]
                        f.flush()
                    # self._start_timer()
                    # self.sendresp( "NACK2:", self.addr[0], self.addr[1])
            except Exception as e:
                # self.sendresp( "NACK:3", self.addr[0], self.addr[1])
                self.logger.info(e)

