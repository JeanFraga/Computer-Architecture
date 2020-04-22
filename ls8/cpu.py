"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.stack_pointer = -1
        # self.instruction_registry = 0 
        self.instruction_registry = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
        }

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            program += '.ls8'
            # print(program)
            with open('Computer-Architecture/ls8/examples/'+program) as f:
                for line in f:
                    line = line.split('#')
                    line = line[0].strip()
                    if line == '':
                        continue
                    self.ram[address] = int(line, 2)
                    address += 1
            
        except:
            print("invalid program name")
            self.HLT()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        while True:
            op = self.ram[self.pc]
            instruction = self.instruction_registry[op]
            instruction()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def HLT(self):
        sys.exit(0)

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[address] = value
        self.pc += 3

    def PRN(self):
        address = self.ram_read(self.pc + 1)
        print(self.reg[address])
        self.pc += 2

    def MUL(self):
        address1 = self.ram_read(self.pc + 1)
        address2 = self.ram_read(self.pc + 2)
        # value1 = self.ram_read(self.pc - 6)
        # value2 = self.ram_read(self.pc - 3)
        # print(self.reg[address1])
        result = self.reg[address1] * self.reg[address2]
        # result = value1 * value2
        self.reg[address1] = result
        # print(self.reg[address1],self.reg[address2],result)
        self.pc += 3
    
    def PUSH(self):
        if self.stack_pointer == 0:
            self.stack_pointer -=1
        address = self.ram_read(self.pc + 1)
        value = self.reg[address]
        self.ram_write(self.stack_pointer, value)
        self.stack_pointer -= 1
        self.pc += 2

    def POP(self):
        if self.stack_pointer < 0:
            self.stack_pointer += 1
            address = self.ram_read(self.pc + 1)
            value = self.ram_read(self.stack_pointer)
            self.reg[address] = value
            self.pc += 2

