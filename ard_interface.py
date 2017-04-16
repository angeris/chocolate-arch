# An interface for the arduino
# There is no support for bad input.

import sys
import serial as ser
import time

ARD_NAME = '/dev/cu.wchusbserial1420'
BITRATE = 9600

ard = ser.Serial(ARD_NAME, BITRATE, timeout=None)
time.sleep(3)

def convert(num):
    if (num.startswith('0x')):
        return int(num, 16)
    else:
        return int(num)

def read(num_bytes, address):
    
    ard.write(chr(1))  # notfiy reading
    ard.write(chr(address))  # notfiy address
    ard.write(chr(num_bytes))  # specify size

    time.sleep(.01)

    for i in range(0, num_bytes):
        print(hex(ord((ard.read()))))
        time.sleep(0.002)

def write(file_name, address):
    f = open(file_name, 'rb')
    data = f.read()

    ard.write(chr(0))  # notify writing
    ard.write(chr(address))  # specify address
    ard.write(chr(len(data)))  # specify size
    
    for c in data:
        ard.write(c)

def clear():
    ard.write(10)



print("[rwc] [filename or size] [address]")
print("q to quit")

cmd = raw_input("Command: ")
while (cmd != 'q'):
    args = cmd.split()
    if (args[0] == 'r'):
        size = convert(args[1])
        addr = convert(args[2])
        read(size, addr)
    elif (args[0] == 'w'):
        file_name = args[1]
        addr = convert(args[2])
        write(file_name, addr)
    elif (args[0] == 'c'):
        clear()

    cmd = raw_input("Command: ")

ard.close()
