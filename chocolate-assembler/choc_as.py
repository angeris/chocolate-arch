# The assembler
import re

BIT = {'nop':0b00, 'and':0b01, 'or':0b10, 'not':0b11}   # bit ops
ATH = {'add':0b00, 'sub':0b01, 'sl':0b10, 'sr':0b11}    # arithmetic ops
LOS = {'SPECIAL':0b00, 'st':0b01, 'ld':0b10, 'li':0b11} # load/store ops
BRC = {'bz':0b00, 'bnz':0b01, 'jz':0b10, 'jnz':0b11}    # branch ops
SPC = {'ln':0b00, 'mov':0b01, 'pop':0b10, 'push':0b11}  # special ops

r0 = 0
r1 = 1
r2 = 2
r3 = 3
res = 3

opcodes = []

def plus(val):
    opcodes.append(val)


# general ops
def arith(instr, a, b):
    return 0b01 << 6 | a << 4 | b << 2 | ATH[instr]

def bitw(instr, a, b):
    return 0b00 << 6 | a << 4 | b << 2 | BIT[instr]

def load_store(instr, a, b):
    if(instr == 'li'):
        temp = {0: 0b00, 1: 0b01, -1: 0b11}
        return 0b10 << 6 | a << 4 | temp[b] << 4 | LOS[instr]
    return 0b10 << 6 | a << 4 | b << 2 | LOS[as_t.instr]

def branch(instr, a, b):
    return 0b11 << 6 | a << 4 | b << 2 | BRC[instr]

def special(instr, a):
    return 0b10 << 6 | a << 4 | SPC[instr] << 2 | 0b00


# bit ops
def nop():
    plus(0)

def _and(a, b):
    plus(bitw('and', a, b))

def _or(a, b):
    plus(bitw('or', a, b))

def _not(a, b):
    plus(bitw('not', a, b))


# arithmetic ops
def add(a, b):
    plus(arith('add', a, b))

def sub(a, b):
    plus(arith('sub', a, b))

def sl(a, b):
    plus(arith('s;', a, b))

def sr(a, b):
    plus(arith('sr', a, b))


# load/store ops
def st(a, b):
    plus(load_store('st', a, b))

def ld(a, b):
    plus(load_store('ld', a, b))

def li(a, b):
    plus(load_store('li', a, b))


# special ops
def ln(a):
    plus(special('ln', a))

def mov(a):
    plus(special('mov', a))

def pop(a):
    plus(special('pop', a))

def push(a):
    plus(special('push', a))



# branch ops
def bz(s, t):
    plus(branch('bz', s, t))

def bnz(s, t):
    plus(branch('bnz', s, t))

def jz(s, t):
    plus(branch('jz', s, t))

def jnz(s, t):
    plus(branch('jnz', s, t))

