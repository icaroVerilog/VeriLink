`include "interface_modified.v"
`default_nettype none

module tb_interface;
    reg clk;
    reg rst;
    reg [15:0] data_in;
    reg [15:0] counter;

    interface interface(
        .clk(clk),
        .rst(rst),
        .data(data_in)
    );

    reg [15:0] data [0:10];

    initial begin
        $readmemb("test.bin", data);
        $dumpfile("tb_interface_modified.vcd");
        $dumpvars(0, tb_interface);

        clk = 1'b0;
        rst = 1'b1;
        data_in = 16'b0000000000000000;
        counter = 16'b0000000000000000;
    end

    always @(posedge clk) begin
        rst <= 1'b0;
        data_in <= data[counter];
        counter <= counter + 1'b1;

        if (counter == 16'b0000000000001000) begin
            $finish;
        end
    end

    always #2 clk = ~clk;
endmodule