# An interface for the arduino
# There is no support for bad input.

import sys
import serial as ser
import time

ARD_NAME = '/dev/cu.wchusbserial1420'
BITRATE = 9600

ard = ser.Serial(ARD_NAME, BITRATE, timeout=None)
cmd = sys.argv[1]
time.sleep(3);

def read(num_bytes):
    
    ard.write('\x01')  # notfiy reading
    ard.write('\x00')  # notfiy reading
    ard.write(chr(num_bytes))  # specify size

    time.sleep(.01);

    for i in range(0, num_bytes):
        print(ard.read())
        time.sleep(0.002)
        
    #print(ard.read(num_bytes))


def write():
    file_name = sys.argv[2]  # get file

    f = open(file_name, 'rb')
    data = f.read()

    ard.write('\x00')  # notify writing
    ard.write('\x00')
    ard.write(chr(len(data)))  # specify size
    for c in data:
        ard.write(c)


def clear():
    ard.write(10)


if (cmd == '-r'):
    n = int(sys.argv[2])
    read(n)
elif (cmd == '-w'):
    write()
    read(2)
else:
    clear()

ard.close()
