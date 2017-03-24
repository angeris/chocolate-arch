# chocolate-arch
Chocolate: a microarchitecture small enough to be implemented on a Lattice HX1K FPGA.

Chocolate is an 8-bit, toy architecture on a single cycle  which fits entirely on an ICEStick. It was implemented as a side project in order to improve my understanding of both digital architecture and Verilog (along with having a bit of fun). Most of the instruction set was written

[NOTES for how to run and such should be put here]

# Instruction set
## Instruction Layout

The instruction set can be decomposed into essentially four kinds of instructions: bit, arithmetic, branches, and loads. The layout is as follows:

1.  `instr[0:1]`: specifies the kind of instruction.
    1. `instr[0:1] == 0b00`: Bit-wise operation.
    2. `instr[0:1] == 0b01`: Arithmetic operation.
    3. `instr[0:1] == 0b10`: Branch operation.
    4. `instr[0:1] == 0b11`: Load/Store operation.

2. 