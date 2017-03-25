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

In Chocolate, the `pc` (Program Counter) and `sp` (Stack pointer) registers are not explicitly accessible and their value can only be manipulated by the use of branch or load/store instructions, respectively.

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
Bit-wise operations have TYPE `instr[7:6] == 0b00`.

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
Bit-wise operations have TYPE `instr[7:6] == 0b01`.

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

*Instruction format:*
```
0b01sstt11
```
*Notes:*

> Note the order. This is `res <- rs >> rt`.

## Load/Store Operations
Load/store operations have TYPE `instr[7:6] == 0b10`.

There are 4 possible lload/store (LS) operations: a special LS (which includes loading the next byte [at PC+1] and popping/pushing from the stack and moving values from `res` to other registers), an LS register instruction, and a load 2-bit, sign-extended immediate (for loading simple constants like 0, -1, and 1).

### LS Special
The load/store special instruction is an instruction that contains 3 different possible behaviours. The behaviour is given by bits `0bvv`.

*Instruction format:*
```
0b10ssvv00
```

When `0bvv==0b00` the processor will load the next word (found at PC+1) onto register `rs` and skip PC to PC+2. This is useful for loading longer immediates into the registers. This is refered to, throughout, as a Load Next.

When `0bvv==0b01` the processor will move the contents of register `res` into register `rs`.

When `0bvv==b1y`, the processor will pop (if `0by==0b0`) or push (if `0by==0b1`) from the stack and increment/decrement the stack pointer accordingly. If the stack pointer is already at the highest memory address, this will place a `0xff` into the register in question.

*Notes:*

> This is a relatively special instruction since it is the only other non-branching instruction that can also control the PC. I'm sure it's going to be quite interesting to debug.

### Store Reg
The store reg instruction stores whatever is in `rs` into `{PC[15:8], rt[7:0]}`. It is therefore not a relative store.

*Instruction format:*
```
0b10sstt01
```

*Notes:*

> For this iteration, I'm unsure whether to just change this to storing `res` into `{rs, rt}` which would allow arbitrary stores, but would certainly make it more complicated.

### Load Reg
The load reg instruction loads whatever is in `{PC[15:8], rt[7:0]}` into `rs`.

*Instruction format:*
```
0b10sstt10
```

*Notes:*

> This has a similar note to the previous. Additionally, it would be interesting to use something of the like to pass longer arguments. I will write an example specifying this.

### Load Immediate
The load immediate instruction loads a sign-extended version of whatever is in the `0bii` part of the section.

*Instruction format:*
```
0b10ssii11
```

*Notes:*

> I made this instruction since I didn't want every load for simple constants like 0, 1, or -1 to have to take a load next and its corresponding byte (therefore taking *two* operations and being a pain to write).

## Branch operations
Branch operations have TYPE `instr[7:6] == 0b11`.

There are 4 possible branching operations which can be split into two types: a relative branch and an absolute branch. Note that all are conditional! In general, for absolute branches it is possible to use the concatenation of any two registers in order to branch to the given address (any 16-bit number).

### Relative branch on zero
The relative branch on zero instruction checks if a register is equal to zero and branches to `PC+rs` if so (where `rs` is sign-extended).

*Instruction format:*
```
0b11sstt00
```

*Notes:*
> None.

### Relative branch on not equal to zero
This relative branch instruction checks if a register `rs` not equal to zero and branches to `PC+rt` if so (where `rt` is sign-extended).

*Instruction format:*
```
0b11sstt01
```

*Notes:*
> None.

### Absolute branch on zero
The relative branch on zero instruction checks if register `res` is equal to zero and branches to `{rs, rt}` if so.

*Instruction format:*
```
0b11sstt10
```

*Notes:*
> None.

### Absolute branch on not equal to zero
The relative branch on zero instruction checks if register `res` is not equal to zero and branches to `{rs, rt}` if so.

*Instruction format:*
```
0b11sstt11
```

*Notes:*
> None.

