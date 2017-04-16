module pc_instr (
    input wire jmp,
    input wire [7:0] addr,

    input wire clk,
    input wire load_imm,

    output wire rw_mem,
    input wire [7:0] read_mem,
    output wire [7:0] write_mem,

    output wire [7:0] instr
);

reg [7:0] pc = 0;
reg is_input = 0;

assign rw_mem = ~is_input;
assign write_mem = pc;


// On the positive edge, update the counter and set the new address to be read
always @(posedge clk) begin
    pc <= jmp ? addr : pc + 1;
    // pc <= pc + 1;
    is_input <= 1;
end

// On the negative edge, read in the value at address
always @(negedge clk) begin
    is_input <= 0;
end


endmodule