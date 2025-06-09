import sys
import math

def ind(value):
    indentation = ""
    for index in range(value):
        indentation = indentation + "\t"
    return indentation

def break_line():
    return "\n";

class ParameterReader:
    def __init__(self):
        self.__parameters = {
            "source_bitwidth": None, 
            "destination_bitwidth": None,
            "output_bitwidth": None,
            "trigger_edge": "p"
        }

    def read(self, parameters):
        parameters.pop(0)

        for index in range(len(parameters)):
            if (parameters[index] == "-s" and parameters[index+1].isdigit()):
                self.__parameters["source_bitwidth"] = parameters[index+1]
            if (parameters[index] == "-d" and parameters[index+1].isdigit()):
                self.__parameters["destination_bitwidth"] = parameters[index+1]
            if (parameters[index] == "-o" and parameters[index+1].isdigit()):
                self.__parameters["output_bitwidth"] = parameters[index+1]
            if (parameters[index] == "-e"):
                if (parameters[index+1] != "p" and parameters[index+1] != "n"):
                    print("ERRO")
                self.__parameters["trigger_edge"] = parameters[index+1]

        return self.__parameters

class ConstructGenerator:
    def generate_wire(self, name, width, cardinality=""):
        if (cardinality != ""):
            cardinality = cardinality + " "

        if (width > 1):
            return f"{cardinality}wire [{width-1}:0] {name};\n"
        else:
            return f"{cardinality}wire {name};\n"
    
    def generate_register(self, name, width, cardinality=""):
        if (cardinality != ""):
            cardinality = cardinality + " "

        if (width > 1):
            return f"{cardinality}reg [{width-1}:0] {name};\n"
        else:
            return f"{cardinality}reg {name};\n"
    
    def generate_atribution(self, l_value, r_value, type):
        return f"{l_value} {type} {r_value};"
    
    # def generate_instantiation(self):
    #     return "module"

    def generate_always(self, edge, body):

        if (edge == "p"):
            src = ind(1) + f"always @(posedge clk) begin\n{body}{ind(1)}end\n"

        return src

    def to_bin(self, value, num_bits):
        if value < 0:
            raise ValueError("O valor deve ser não negativo.")
        if num_bits <= 0:
            raise ValueError("O número de bits deve ser positivo.")
        
        binary = bin(value)[2:]
        
        bin_str = binary.zfill(num_bits)
        
        if len(binary) > num_bits:
            raise ValueError(f"O valor {value} não pode ser representado em {num_bits} bits.")
        
        return bin_str
        
class InterfaceGenerator(ConstructGenerator):
    def __init__(self, parameters):
        self.__buffer_qnt = math.ceil(int(parameters["source_bitwidth"]) / int(parameters["destination_bitwidth"]))
        self.__assigned_buffers = []
        self.__buffer_full = []
        self.__buffer_list = []
        self.__current_buffer = 0
        self.__counter_needed_bw = 0
        self.src_bw = int(parameters["source_bitwidth"])
        self.dest_bw = int(parameters["destination_bitwidth"])
        self.out_bw = int(parameters["output_bitwidth"])

    def execute(self):

        horizontal_board = ""
        horizontal_board += "//     \u2554"
        horizontal_board += "\u2550" * 48
        horizontal_board += "\u2557\n"
        horizontal_board += "//     \u2551  This code is licensed under the MIT License.  \u2551\n"
        horizontal_board += "//     \u2551  Modify this module according to your needs.   \u2551\n"
        horizontal_board += "//     \u255A"
        horizontal_board += "\u2550" * 48
        horizontal_board += "\u255D\n"
        horizontal_board += "\n\n"

        src = ""
        src += horizontal_board
        src += "module interface (\n"
        src += ind(1) + "clk,\n"
        src += ind(1) + "rst,\n"
        src += ind(1) + "data_in,\n"
        src += ind(1) + "data_out\n"
        src += ");"


        src += break_line()
        src += ind(1) + generator.generate_wire("clk", 1, "input")
        src += ind(1) + generator.generate_wire("rst", 1, "input")
        src += ind(1) + generator.generate_wire("data_in", self.src_bw, "input")
        src += break_line()
        src += ind(1) + generator.generate_wire("data_out", self.out_bw, "output")
        src += break_line()

        for index in range(self.__buffer_qnt):
            src += ind(1) + generator.generate_register(f"buffer{index}", int(parameters["destination_bitwidth"]), "")
        src += ind(1) + generator.generate_register(f"buffer_aux", int(parameters["destination_bitwidth"]), "")
        src += break_line()
        src += ind(1) + generator.generate_register("valid_data", self.__buffer_qnt)
        src += ind(1) + "`"
        src += break_line()
        src += self.generate_always("p")
        src = src.replace("`",generator.generate_register("counter", self.__counter_needed_bw))
        src += "endmodule"
        return src
    
    def __buffers_already_assigned(self):
        assigned = self.__assigned_buffers
        buffers = self.__buffer_list

        assigned.sort()
        buffers.sort()

        if (assigned == buffers):
            return True
        else:
            return False

    def __get_buffer(self):
        if (self.__current_buffer == len(self.__buffer_list)):
            self.__current_buffer = 0
        buffer = self.__buffer_list[self.__current_buffer]
        self.__current_buffer = self.__current_buffer + 1
        return buffer

    def __verify_stop_condition(self, conf_possibilities):
        if (len(conf_possibilities) > 1):
            first:list = conf_possibilities[0]   
            last:list = conf_possibilities[len(conf_possibilities) - 1]

            for index in range(len(first)):
                if (first[index][1] != last[index][1]):
                    return False
            return True
        else:
            return False

    def __needed_bit_quantity(self, value):
        if value < 0:
            return 0 
        if value == 0:
            return 1
        return math.floor(math.log2(value)) + 1

    def generate_buffer_assignment(self):
        conf_possibilities = []
        max_bits = 0
        p = 0

        for index in range(self.__buffer_qnt):
            self.__buffer_list.append(index)
            self.__buffer_full.append(0)
        while (True):
            max_bits = self.src_bw
            iteration = []
            while (True):
                if (max_bits > self.dest_bw):
                    if (p > 0):
                        pair = []
                        pair.append(self.__get_buffer())
                        pair.append(p)
                        iteration.append(pair)
                        max_bits = max_bits - p
                        p = 0
                    else:
                        pair = []
                        pair.append(self.__get_buffer())
                        pair.append(self.dest_bw)
                        iteration.append(pair)
                        max_bits = max_bits - self.dest_bw
                elif (max_bits == self.dest_bw):
                    pair = []
                    pair.append(self.__get_buffer())
                    pair.append(max_bits)
                    iteration.append(pair)
                    max_bits = 0

                    break
                elif (max_bits < self.dest_bw):
                    pair = []
                    pair.append(self.__get_buffer())
                    pair.append(max_bits)
                    iteration.append(pair)
                    p = self.dest_bw - max_bits

                    break
            conf_possibilities.append(iteration)

            if (iteration[len(iteration) - 1][1] != self.dest_bw):
                self.__current_buffer = iteration[len(iteration) - 1][0]

            if (self.__verify_stop_condition(conf_possibilities)):
                conf_possibilities.pop()
                break

        conditional_structure_counter = 0
        src = ""

        carry = 0
        simple_carry = 0
        carry_lower_bit = 0

        for conf in conf_possibilities:
            needed_bit_quantity = self.__needed_bit_quantity(len(conf_possibilities) - 1)

            self.__counter_needed_bw = needed_bit_quantity

            binary_value = generator.to_bin(
                conditional_structure_counter, 
                needed_bit_quantity
            )

            src += ind(3) + f"if (counter == {needed_bit_quantity}'b{binary_value}) begin\n"
            lower_bit = 0
            upper_bit = 0
            for index in range(len(conf)):
                if (carry == 0):
                    upper_bit = (lower_bit + conf[index][1]) - 1
                    if (self.__buffers_already_assigned()):
                        src += ind(4) + f"buffer_aux <= data_in[{upper_bit}:{lower_bit}];\n"
                        carry = upper_bit - lower_bit
                        carry_lower_bit = lower_bit
                    else:
                        if (simple_carry != 0):
                            src += ind(4) + f"buffer{conf[index][0]}[{self.dest_bw - 1}:{simple_carry}] <= data_in[{upper_bit}:{lower_bit}];\n"
                            simple_carry = 0
                        else:
                            src += ind(4) + f"buffer{conf[index][0]} <= data_in[{upper_bit}:{lower_bit}];\n"
                        
                        if (((upper_bit - lower_bit + 1) != self.dest_bw) and (index == len(conf) - 1)):
                            simple_carry = upper_bit - lower_bit + 1
                        self.__assigned_buffers.append(conf[index][0])
                    lower_bit = upper_bit + 1
                else:
                    upper_bit = (lower_bit + conf[index][1]) - 1
                    if (self.__buffers_already_assigned()):
                        src += ind(4) + f"buffer_aux <= data_in[{upper_bit}:{lower_bit}];\n"
                        carry = upper_bit - lower_bit
                        carry_lower_bit = lower_bit
                    else:
                        carry_lower_bit = 0
                        src += ind(4) + f"buffer{conf[index][0]} <= {{buffer_aux[{carry_lower_bit + carry}:{carry_lower_bit}], data_in[{upper_bit}:{lower_bit}]}};\n"
                        carry = 0
                    lower_bit = upper_bit + 1
                self.__buffer_full[conf[index][0]] = self.__buffer_full[conf[index][0]] + conf[index][1]
            
            valid_data_conf = ""
            for index in range(self.__buffer_qnt):
                if (self.__buffer_full[index] >= self.dest_bw):
                    valid_data_conf = valid_data_conf + "1"
                    self.__buffer_full[index] = self.__buffer_full[index] - self.dest_bw
                else:
                    valid_data_conf = valid_data_conf + "0"
            src += ind(4) + f"valid_data <= {self.__buffer_qnt}'b{valid_data_conf};\n"


            self.__assigned_buffers = []
            

            conditional_structure_counter = conditional_structure_counter + 1

            if(conditional_structure_counter == len(conf_possibilities)):
                src += ind(4) + f"counter <= {needed_bit_quantity}'b{generator.to_bin(0, needed_bit_quantity)};\n"
            else:
                src += ind(4) + "counter <= counter + 1'b1;\n"     

            src += ind(3) + "end\n" 
        return src
    
    def generate_always(self, edge):
        if (edge == "p"):
            src = ind(1) + f"always @(posedge clk) begin\nx\n{ind(1)}end\n"
        elif (edge == "n"):
            src = ind(1) + f"always @(negedge clk) begin\nx\n{ind(1)}end\n"

        always_src = ind(2) + f"if (rst) begin\n"
        for index in range(self.__buffer_qnt):
            always_src += ind(3) + f"buffer{index} <= {self.dest_bw}'b{generator.to_bin(0, self.dest_bw)};\n"
        if (self.src_bw % self.dest_bw != 0):
            always_src += ind(3) + f"buffer_aux <= {self.dest_bw}'b{generator.to_bin(0, self.dest_bw)};\n"
        always_src += ind(3) + f"valid_data <= {self.__buffer_qnt}'b{generator.to_bin(0, self.__buffer_qnt)};\n"

        always_src += ind(3) + f"counter <= ç'b*;\n"
        always_src += ind(2) + "end\n"
        always_src += ind(2) + "else begin\n"
        always_src += self.generate_buffer_assignment()
        always_src = always_src.replace("ç",str(self.__counter_needed_bw))
        always_src = always_src.replace("*",generator.to_bin(0, self.__counter_needed_bw))
        always_src += ind(2) + "end"
        src = src.replace("x", always_src)
        return src

parameter_reader = ParameterReader()
generator = ConstructGenerator()

parameters = parameter_reader.read(sys.argv)

interfaceGenerator = InterfaceGenerator(parameters)
src = interfaceGenerator.execute()


with open("interface.v", "w", encoding="utf-8") as arquivo:
    arquivo.write(src)
