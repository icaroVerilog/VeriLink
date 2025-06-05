module interface (
	clk,
	rst,
	data,
);
	input wire clk;
	input wire rst;
	input wire [0:20] data;

	reg [9:0] buffer0;
	reg [9:0] buffer1;
	reg [9:0] buffer2;
	reg [9:0] buffer_aux;

	always @(posedge clk) begin
		if (rst) begin
			buffer0 <= 10'b0000000000;
			buffer1 <= 10'b0000000000;
			buffer2 <= 10'b0000000000;
			buffer_aux <= 10'b0000000000;
			valid_data0 <= 1'b0;
			valid_data1 <= 1'b0;
			valid_data2 <= 1'b0;
			counter <= 0'b0000000000;
		end
		else begin
			if (counter == 4'b0000) begin
				buffer0 <= data[9:0];
				buffer1 <= data[19:10];
				buffer2 <= data[20:20];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b0;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0001) begin
				buffer2[9:1] <= data[8:0];
				buffer0 <= data[18:9];
				buffer1 <= data[20:19];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b0;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0010) begin
				buffer1 <= data[7:0];
				buffer2 <= data[17:8];
				buffer0 <= data[20:18];
				valid_data0 <= 1'b0;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0011) begin
				buffer0 <= data[6:0];
				buffer1 <= data[16:7];
				buffer2 <= data[20:17];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b0;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0100) begin
				buffer2 <= data[5:0];
				buffer0 <= data[15:6];
				buffer1 <= data[20:16];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b0;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0101) begin
				buffer1 <= data[4:0];
				buffer2 <= data[14:5];
				buffer0 <= data[20:15];
				valid_data0 <= 1'b0;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0110) begin
				buffer0 <= data[3:0];
				buffer1 <= data[13:4];
				buffer2 <= data[20:14];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b0;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b0111) begin
				buffer2 <= data[2:0];
				buffer0 <= data[12:3];
				buffer1 <= data[20:13];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b0;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b1000) begin
				buffer1 <= data[1:0];
				buffer2 <= data[11:2];
				buffer0 <= data[20:12];
				valid_data0 <= 1'b0;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b1;
				counter <= counter + 1'b1;
			end
			if (counter == 4'b1001) begin
				buffer0 <= data[0:0];
				buffer1 <= data[10:1];
				buffer2 <= data[20:11];
				valid_data0 <= 1'b1;
				valid_data1 <= 1'b1;
				valid_data2 <= 1'b1;
				counter <= 4'b0000;
			end
		end
	end
endmodule