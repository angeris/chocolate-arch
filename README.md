# Chocolate-Arch
Chocolate: a microarchitecture small enough to be implemented on a Lattice HX1K FPGA.

Chocolate is an 8-bit, single-cycle, toy architecture which fits entirely on an ICEStick. It was implemented as a side project in order to improve my understanding of both digital architecture and Verilog (along with having a bit of fun). It can also be used as an accessible introduction to low-level systems and how they work.

[NOTES for how to run and such should be put here]

# Register layout
There are four general-purpose registers in Chocolate which are refered to as `r0`, `r1`, `r2`, and `r3`. The last one also has a second shorthand as `res` since it is specifically designed to be the result register. The result of any arithmetic or bitwise operation is immediately put in this register. As expected, the registers have the following numbering
```
r0: 0b00
r1: 0b01
r2: 0b10
res: 0b11
```

In Chocolate, the PC (Program Counter) register is not an explicitly accessible register and its value can only be manipulated by the use of branch instructions.

# Instruction Set
## Instruction layout
The instruction set can be decomposed into essentially four kinds of instructions: bit, arithmetic, branches, and loads. The layout is as follows.

`instr[7:6]`, the two MSBs specify the kind of instruction that this opcode is. There are four such types:
1. `instr[7:6] == 0b00`: Bit-wise operation.
2. `instr[7:6] == 0b01`: Arithmetic operation.
3. `instr[7:6] == 0b10`: Branch operation.
4. `instr[7:6] == 0b11`: Load/Store operation.

Almost every instruction has the form
```
TYPE [7:6], rs [5:4], rt [3:2], OP [1:0]
```
where `OP` is a special 2-bit number representing either the type of operation being performed (in the case of arithmetic or bit operations) or the type of load or branch which this operation signifies. `rt` and `rs` are the register indexes such that, for some operation `*` we have
```
res = (rs) * (rt)
```
for most arithmetic and bitwise instructions. Throughout isntructions, `rs` will be given as `0bss`, `rt` will be given as `0btt`, and "don't matter" bits will be given as `0bxx` such that an example instruction will have the form
```
0b00sstt01
```
for a general AND instruction.

## Bit-wise operations
Bit-wise operations have `TYPE` `instr[7:6] == 0b00`.

There are 4 kinds of bitwise operations: NOP, AND, OR, and NOT, each of which is applied to two (or one/none, in the case of NOT/NOP respectively) register and the result is placed in the `res` register.

### NOP
General NOP instruction that doesn't do anything.

*Instruction format:*
```
0b00xxxx00
```

*Notes:*

>I am thinking there might be something fun to do with the unused bits, but I didn't want to add complexity in the first iteration of this instruction set. If you have any fun ideas, send me a line!

### AND
Takes the bitwise AND of `rs` and `rt` and stores the result in `res`.

*Instruction format:*
```
0b00sstt01
```
*Notes:*

> None.

### OR
Takes the bitwise OR of `rs` and `rt` and stores the result in `res`.

*Instruction format:*
```
0b00sstt10
```
*Notes:*

> None.

### NOT
Takes the bitwise NOT of `rt` and stores the result in `rs`.

*Instruction format:*
```
0b00sstt11
```
*Notes:*

> I decided on this since there were two extra bits to play with. Since I didn't implement a branch on greater than zero, this allows for a little more flexibility in using arbitrary registers.


## Arithmetic operations
Bit-wise operations have `TYPE` `instr[7:6] == 0b01`.

There are 4 kinds of bitwise operations: ADD, SUB (subtract), SL (shift left), and SR (shift right), each of which is applied to two registers and the result is placed in the `res` register.

### ADD
Adds the contents of `rs` and `rt` and stores the result in `res`.

*Instruction format:*
```
0b01sstt00
```
*Notes:*

> None.

### SUB
Subtracts the contents of `rt` from `rs` and stores the result in `res`.

*Instruction format:*
```
0b01sstt01
```
*Notes:*

> Note the order. This is `res <- rs - rt`.

### SL
Left-shifts the contents of `rs` by `rt` and stores the result in `res`.

*Instruction format:*
```
0b01sstt10
```
*Notes:*

> Note the order. This is `res <- rs << rt`.

### SR
Right-shifts the contents of `rs` by `rt` and stores the result in `res`.