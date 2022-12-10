from lib import io

class CPU:
    def __init__(self):
        self.clock_cycle = 1
        self.x = 1
        self.instructions = None
        self.signal_strengths = []
        self.crt = CRT()

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
            print(f"instruction: {' '.join(instruction)}")
            opcode = instruction[0]
            operand = instruction[1] if len(instruction) == 2 else ""
            if opcode == "noop":
                self.clock_cycle += 1    # Do nothing for a clock cycle before moving on.
                self.sample_signal_strength()
                print(f"clock_cycle: {self.clock_cycle}")
                self.crt.draw_pixel(sprite_centre=self.x, cur_pixel=self.clock_cycle)
            elif opcode == "addx":
                self.clock_cycle += 1    # Start executing the operation.
                print(f"clock_cycle: {self.clock_cycle}")
                self.crt.draw_pixel(sprite_centre=self.x, cur_pixel=self.clock_cycle)
                self.sample_signal_strength()
                self.clock_cycle += 1    # Operation finishes after this cycle.
                print(f"clock_cycle: {self.clock_cycle}")
                self.x += int(operand)
                self.crt.draw_pixel(sprite_centre=self.x, cur_pixel=self.clock_cycle)
                self.sample_signal_strength()
        self.crt.render_display()


class CRT:
    def __init__(self):
        self.pixels_per_row = 40    # Used for drawing the display.
        self.sprite_width = 1       # Number of pixels around the sprite centre that can be lit.
        # self.cur_pixel = 0          # Which pixel the CRT will light up if commanded to.
        self.sprite_centre = 0      # Location of sprite on the display.
        self.display = ""           # What is visible on the display.

    def draw_pixel(self, sprite_centre, cur_pixel):
        cur_pixel = (cur_pixel - 1) % self.pixels_per_row   # Ensures cur_pixel aligns with display's 0-indexing.
        # sprite_centre -= 1  # Ensures sprite_centre aligns with display's 0-indexing.
        print(f"cur_pixel: {cur_pixel}")
        lower_limit = sprite_centre - self.sprite_width
        upper_limit = sprite_centre + self.sprite_width
        print(f"lower_limit: {lower_limit}")
        print(f"sprite_centre: {sprite_centre}")
        print(f"upper_limit: {upper_limit}")
        if cur_pixel >= lower_limit and cur_pixel <= upper_limit:
            print("Drawing lit pixel.")
            self.display += "#"
        else:
            print("Drawing dark pixel.")
            self.display += "."
        if cur_pixel % self.pixels_per_row == 0:
            self.display += "\n"
        print()

    def render_display(self):
        print(self.display)



print("Advent of Code 2022 Day 10")
print("-------------------------")

program = io.file_to_list("input/day-10-test-data.txt")
# program = io.file_to_list("input/day-10-input.txt")

instructions = [line.split() for line in program]
cpu = CPU()
cpu.load_program(instructions)
cpu.run()
signal_strengths = cpu.get_signal_strengths()

# print(f"signal_strengths: {signal_strengths}")
print("PART 1")
print("======")
print(f"Sum of 20th, 60th, 100th, 140th, 180th, and 220th signal strengths: {sum([s[1] for s in signal_strengths])}")
print("======")
# Attempt 1: 13820
