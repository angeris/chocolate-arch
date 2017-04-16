from choc_as import *

ln(r0)  # 0x0
word(0x8)
jz(r0, r0)
nop()  
nop()  # 0x4
nop()
nop()
nop()
jz(r1, r1)  # 0x8


qcompile('code.hex')
