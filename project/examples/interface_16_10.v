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
	reg [9:0] buffer_aux;

	always @(posedge clk) begin
		if (rst) begin
			buffer0 <= 10'b0000000000;
			buffer1 <= 10'b0000000000;
			buffer_aux <= 10'b0000000000;
			valid_data0 <= 1'b0;
			valid_data1 <= 1'b0;
			counter <= 3'b000;
		end
		else begin
			if (counter == 3'b000) begin
				buffer0 <= data[9:0];
				buffer1 <= data[15:10];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b0;
				counter <= counter + 1'b1;
			end
			if (counter == 3'b001) begin
				buffer1[9:6] <= data[3:0];
				buffer0 <= data[13:4];
				buffer_aux <= data[15:14];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 3'b010) begin
				buffer1 <= {buffer_aux[1:0], data[7:0]};
				buffer0 <= data[15:8];
				valid_data0 <= 1'b0;
				valid_data1 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 3'b011) begin
				buffer0[9:8] <= data[1:0];
				buffer1 <= data[11:2];
				buffer_aux <= data[15:12];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 3'b100) begin
				buffer0 <= {buffer_aux[3:0], data[5:0]};
				buffer1 <= data[15:6];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				counter <= 3'b000;
			end
		end
	end
endmodule