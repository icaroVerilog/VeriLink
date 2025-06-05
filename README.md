# Verilink


Verilink is an open-source project designed to generate interfaces between Verilog modules in order to maximize the utilization of input bits, thereby avoiding the underuse of data transfer resources, which are often the main limiting factor in most devices. Fully modular in design, it allows the creation of a modular interface that efficiently transfers data from a source with a larger bit width to multiple destinations that use a smaller bit width.


![Interface Architecture Diagram](https://github.com/icaroVerilog/VeriLink/blob/main/images/architecture.png)


## Utilization
Verilink requires three flags for its operation:

|      Flag      |Description                          |Value Type                         |
|----------------|-------------------------------|-----------------------------|
|-s							 |specifies the number of bits to be received by the interface module        |Integer            |
|-d          		 |specifies the number of bits to be sent to the destination modules            |Integer          |
|-e              |sets the activation edge of the module, with possible values being `p` (positive edge) and `n` (negative edge)|Character