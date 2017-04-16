module decoder(
    input wire [7:0] instr,
    
    output wire [7:0] rs_read,
    output wire [7:0] rt_read,
    output wire is_write,
    output wire [7:0] reg_write,

    output wire is_short_imm,
    output wire is_jump,

    output wire is_load_next,
    output wire [2:0] alu_op
);

assign is_jump = instr[7:6] == 2'b11;
assign is_load_next = instr == 8'h80;



endmodule