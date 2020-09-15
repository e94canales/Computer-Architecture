"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        
        # checks if there is an argument in CLI
        if len(sys.argv) <= 1:
            print(">> No Valid Arguments")
            sys.exit()
        else:
            # stores CLI argument
            arg = sys.argv[1]


        # open/closes file
        with open(arg, "r") as e:

            # confirmation for file opened
            print(f">> Loaded: {e.name.split('/')[-1].upper()}")

            for instruction in e.readlines():

                # strips white space
                instruction = instruction.split("#")[0].strip()
                
                # ignores blank lines
                if not instruction:
                    continue
            
                # loads to ram
                self.ram[address] = int(instruction, 2)
                address += 1    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            ir = self.ram[self.pc]

            # HLT
            if ir == 0b00000001:
                running = False

            # LDI
            if ir == 0b10000010:
                reg_index = self.ram[self.pc + 1]
                data_value = self.ram[self.pc + 2]
                self.reg[reg_index] = data_value
                self.pc += 3
            
            # PRN
            if ir == 0b01000111:
                reg_index = self.ram[self.pc + 1]
                print(f"** {self.reg[reg_index]}")
                self.pc += 2

            # MUL
            if ir == 0b10100010:
                value_one = self.ram[self.pc + 1]
                value_two = self.ram[self.pc + 2]
                print(f">> Multiply: {self.reg[value_one]} x {self.reg[value_two]}")
                self.alu("MUL", value_one, value_two)
                self.pc += 3
