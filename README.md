# Verilink


Verilink is an open-source project designed to generate interfaces between Verilog modules in order to maximize the utilization of input bits, thereby avoiding the underuse of data transfer resources, which are often the main limiting factor in most devices. Fully modular in design, it allows the creation of a modular interface that efficiently transfers data from a source with a larger bit width to multiple destinations that use a smaller bit width.


## Architecture 

For a given input bit width, the software calculates how many outputs with the specified output bit width can be driven. The image below illustrates a use case where the input has 16 bits, but the receiving module only requires 10 bits. In a typical scenario, this would result in 6 bits being underutilized. In this case, however, the interface stores these bits so that another instance or even the same one, depending on the design can be supplied with data, thereby increasing the circuit's throughput.


![Interface Architecture Diagram](https://github.com/icaroVerilog/VeriLink/blob/main/images/architecture.png)


## Utilization
Verilink requires three flags for its operation:

|      Flag      |Description                          |Value Type                         |
|----------------|-------------------------------|-----------------------------|
|-s							 |specifies the number of bits to be received by the interface module        |Integer            |
|-d          		 |specifies the number of bits to be sent to the destination modules            |Integer          |
|-e              |sets the activation edge of the module, with possible values being `p` (positive edge) and `n` (negative edge)|Character