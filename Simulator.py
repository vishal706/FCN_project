import RUDPServer
import RUDPClient
import os
import subprocess

segment_size = 0
buffer_size = 100

SERVER_CMD = f"python3 RUDPServer.py -f \"recv.txt\" -p 101 -i 10.0.0.2 -s {segment_size} -w {buffer_size}"
CLIENT_CMD = f"python3 RUDPClient.py -i 10.0.0.2 -f \"send.txt\" -p 101 -s {segment_size}"

def SimulatingDifferentWindowSizes():
    for i in range(1000):
        print(i)
    return None

def SimulatingDifferentBufferSizes():
    return None

def SimulatingDifferentBandwidth():
    return None

print("hello, world!")
SimulatingDifferentWindowSizes()