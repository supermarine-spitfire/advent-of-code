from queue import Queue

from lib import io

class CPU:
    def __init__(self):
        self.clock_cycle = 1
        self.x = 1
        self.instructions = None
        self.signal_strengths = []

    def load_program(self, instructions):
        self.instructions = instructions

    def sample_signal_strength(self):
        # Signal strength is the current clock cycle multiplied by the value in the x register.
        cycle_base = 20
        if self.clock_cycle == cycle_base or (self.clock_cycle - cycle_base) % 40 == 0:
            self.signal_strengths.append((self.clock_cycle, self.clock_cycle * self.x))

    def get_signal_strengths(self):
        return [s for s in self.signal_strengths]

    def run(self):
        if not self.instructions:
            print("No instructions loaded.")
        for instruction in instructions:
            opcode = instruction[0]
            operand = instruction[1] if len(instruction) == 2 else ""
            if opcode == "noop":
                self.clock_cycle += 1    # Do nothing for a clock cycle before moving on.
                self.sample_signal_strength()
            elif opcode == "addx":
                self.clock_cycle += 1    # Start executing the operation.
                self.sample_signal_strength()
                self.x += int(operand)
                self.clock_cycle += 1    # Finish the operation.
                self.sample_signal_strength()


print("Advent of Code 2022 Day 9")
print("-------------------------")

# program = io.file_to_list("input/day-10-test-data.txt")
program = io.file_to_list("input/day-10-input.txt")

instructions = [line.split() for line in program]
cpu = CPU()
cpu.load_program(instructions)
cpu.run()
signal_strengths = cpu.get_signal_strengths()

print(f"signal_strengths: {signal_strengths}")
print("PART 1")
print("======")
print(f"Sum of 20th, 60th, 100th, 140th, 180th, and 220th signal strengths: {sum([s[1] for s in signal_strengths])}")
print("======")
# Attempt 1: 13820
