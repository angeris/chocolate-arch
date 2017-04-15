#!/usr/bin/python

# An interface for the arduino
# There is no support for bad input.

import sys
import serial as ser

ARD_NAME = '/dev/cu.wchusbserial1420'
BITRATE = 9600

ard = ser.Serial(ARD_NAME, BITRATE)
cmd = sys.argv[1]

def read():
    num_bytes = sys.argv[2] # get number of bytes

    ard.write(1)  # notfiy reading
    ard.write(num_bytes)  # specify size

    for i in range(0, num_bytes):
        print(ard.readline())


def write():
    file_name = sys.argv[2]  # get file

    f = open(file_name, 'rb')
    data = f.read()

    ard.write(0)  # notify writing
    ard.write(len(data))  # specify size
    for c in data:
        ard.write(c)


def clear():
    ard.write(10)


if (cmd == '-r'):
    read()
elif (cmd == '-w'):
    write()
else:
    clear()
