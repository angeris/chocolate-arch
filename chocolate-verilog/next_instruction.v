module n_instr (
    input wire clk,
    input wire is_load_next,

    output wire force_nop,
    output wire load_imm_next
);

reg is_next_load, is_load_after;

assign load_imm_next = is_load_after;

always @(posedge clk) begin
    is_next_load <= is_load_next;
    is_load_after <= is_next_load;
end

assign force_nop = is_load_after;

endmodule