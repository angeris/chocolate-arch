module processor (
    input wire dbg_clk,

    output wire rw_mem,
    inout wire [7:0] mem_io,
    
    output wire pin_led,
);

wire [7:0] instr;
wire [7:0] rom_read;
wire [7:0] rom_write;
wire is_jump;

pc_instr pc_reg (
    .clk(dbg_clk),
    .instr(instr),
    
    .jmp(is_jump),
    .addr(alu_output),

    .read_mem(rom_read),
    .write_mem(rom_write),
    .rw_mem(rw_mem),
);

// If the memory is an input, send the rom_write, otherwise set it to high impedance and read
assign mem_io = rw_mem ? rom_write : 8'bz;
assign rom_read = rw_mem ? 0 : mem_io;
assign pin_led = pc[0];

wire is_write, is_short_imm;
wire [1:0] rs_read;
wire [1:0] rt_read;
wire [1:0] reg_write;
wire [2:0] alu_op;
wire force_nop;

decoder dec (
    .instr(instr),
    .force_nop(force_nop),

    .rs_read(rs_read),
    .rt_read(rt_read),
    .is_write(is_write),
    .reg_write(reg_write),
    .is_short_imm(is_short_imm),

    .is_jump(is_jump),
    
    .is_load_next(is_load_next),
    .alu_op(alu_op)
);


wire [7:0] alu_output;

alu m_alu(
    .alu_op(alu_op),
    .alu_x(rs_val),
    .alu_y(rt_val),

    .alu_output(alu_output)
);

wire [7:0] rs_val;
wire [7:0] rt_val;
wire [7:0] write_val;

wire is_imm_next;

assign write_val = is_imm_next ? instr : alu_output;

regfile registers (
    .clk(dbg_clk),

    .rs(rs_read),
    .rt(rt_read),

    .rs_val(rs_val),
    .rt_val(rt_val),

    .is_write(is_write),
    .reg_write(reg_write),
    .write_val(write_val)
);

n_instr next_instruction (
    .clk(dbg_clk),
    .is_load_next(is_load_next),
    .force_nop(force_nop),
    .load_imm_next(is_imm_next)
);

endmodule