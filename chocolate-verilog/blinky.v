module top(
    input wire clk, //12 MHz clock signal
    
    output wire pin_d5,
    output wire pin_d1,
    output wire pin_d2,
    output wire pin_d3,
    output wire pin_d4
);
    reg led_on = 0;
    reg [1:0] curr_led = 0;
    reg [24:0] curr_time; // Holds the current time

    assign pin_d5 = curr_time[23];

    // Switch pin every 2^24/(12e6) of a second
    always @(posedge clk)
        curr_time <= curr_time + 1;
    always @(posedge curr_time[23])
        curr_led <= curr_led + 1;

    // Do the assignments for the red leds
    assign pin_d1 = (curr_led == 0);
    assign pin_d2 = (curr_led == 1);
    assign pin_d3 = (curr_led == 2);
    assign pin_d4 = (curr_led == 3);

endmodule