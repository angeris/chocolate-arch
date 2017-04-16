module n_instr (
    input wire clk,

    input wire is_load_next,
    input wire [7:0] instr,

    output wire force_nop
);

reg is_next_load, is_load_after;

always @(posedge clk) begin
    is_next_load <= is_load_next;
    is_load_after <= is_next_load;
end

assign force_nop = is_load_after;

endmodule