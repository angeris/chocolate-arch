module regfile(
    input wire clk,

    input wire [1:0] rs,
    input wire [1:0] rt,

    output wire [7:0] rs_val,
    output wire [7:0] rt_val,

    input wire is_write,
    input wire [1:0] reg_write,
    input wire [7:0] write_val
);

reg [7:0] registers [1:0];

reg [7:0] rs_output_buf = 0;
reg [7:0] rt_output_buf = 0;

assign rs_val = register[rs];
assign rt_val = register[rt];

always @(posedge clk) begin
    rs_output_buf <= register[rs];
    rt_output_buf <= register[rt];
end

always @(negedge clk) begin
    if(is_write)
        registers[reg_write] <= write_val;
end

endmodule