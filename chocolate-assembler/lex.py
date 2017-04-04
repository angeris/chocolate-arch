# A little lexer for the assembler
import re

TYPE_BIT = ['nop', 'and', 'or', 'not']      # bit-wise ops
TYPE_ATH = ['add', 'sub', 'sl', 'sr']       # arithmetic ops
TYPE_LOS = ['SPECIAL', 'st', 'ld', 'li']    # load/store ops
TYPE_BRC = ['bz', 'bnz', 'jz', 'jnz']       # branch ops
SPECIAL_INS = ['ln', 'mov', 'push', 'pop']  # special instructions

ALL_TYPES = [TYPE_BIT, TYPE_ATH, TYPE_LOS, TYPE_BRC, SPECIAL_INS]
NAMES_TYPES = ['bit', 'arith', 'load/store', 'branch', 'special']

REGEX_RX = 'r[0-9]'



class AssemblerToken:
    def __init__(line):
        line = line.lower()
        line = re.sub(r'\s\s+',' ',line) # standardize spaces
        instr, args = line.split(' ', 1) # split line
        self.instr = instr

        args_list = re.sub(' ', '', args).split(',')
        for i, instructions in enumerate(ALL_TYPES):
            for j, ins in enumerate(types):

        

    def __str__():
        pass


# Returns a token
def tokenize_line(curr_line):

