module interface (
	clk,
	rst,
	data,
);
	input wire clk;
	input wire rst;
	input wire [0:15] data;

	reg [9:0] buffer0;
	reg [9:0] buffer1;

	always @(posedge clk) begin
		if (rst) begin
			buffer0 <= 10'bNone;
			buffer1 <= 10'bNone;
			buffer_aux <= 10'bNone;
			valid_data0 <= 1'b0;
			valid_data1 <= 1'b0;
			counter <= 0'bNone;
		end
		else begin
			if (counter == 000) begin
			end
			if (counter == 000) begin
			end
			if (counter == 000) begin
			end
			if (counter == 000) begin
			end
			if (counter == 000) begin
			end
		end
	end
endmodule