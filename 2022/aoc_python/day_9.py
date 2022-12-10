from math import sqrt
from lib import io

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        return Point2D(self.x + x, self.y + y)

    def add_x(self, x):
        return self.add(self.x + x, 0)

    def add_y(self, y):
        return self.add(0, self.y + y)

    def subtract(self, x, y):
        return Point2D(self.x - x, self.y - y)

    def subtract_x(self, x):
        return self.add(self.x - x, 0)

    def subtract_y(self, y):
        return self.add(0, self.y - y)

    def scale(self, c):
        return Point2D(self.x * c, self.y * c)

    def euclidean_distance(self, p) -> float:
        return sqrt(pow(p.x - self.x, 2) + pow(p.y - self.y, 2))

    def manhattan_distance(self, p) -> float:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self):
        return f"Point2D({self.x}, {self.y})"

    __repr__ = __str__


def calculate_moves(head_position, tail_position, direction):
    # Move the head.
    previous_head_position = Point2D(head_position.x, head_position.y)
    if direction == "U":
        head_position.y += 1
        print(f"Moving head up: {head_position}")
    elif direction == "D":
        head_position.y -= 1
        print(f"Moving head down: {head_position}")
    elif direction == "L":
        head_position.x -= 1
        print(f"Moving head left: {head_position}")
    elif direction == "R":
        head_position.x += 1
        print(f"Moving head right: {head_position}")
    else:
        pass    # Ignore any other input.

    print(f"Tail position: {tail_position}")
    print(f"Previous head position: {previous_head_position}")
    # Move the tail, if needed.
    # The distance checks test if head and tail are touching or not. Tail moves if the test fails.
    # The tail moves to the previous position of the head.
    if head_position.euclidean_distance(tail_position) >= 2  \
       or head_position.manhattan_distance(tail_position) >= 3:
       # Euclidean distance handles cases where head and tail are in same rows/columns.
       # Manhattan distance handles cases where head and tail are on diagonals.
       tail_position.x = previous_head_position.x
       tail_position.y = previous_head_position.y
       print(f"Moved tail: {tail_position}")

    return head_position, tail_position


def print_tail_positions(max_x, max_y, covered_positions):
    origin = Point2D(0, 0)          # Map everything relative to this point.
    for i in range(max_y, -1, -1):  # Printing from top on down.
        for j in range(max_x + 2):  # Add buffer at end of row.
            cur_point = Point2D(j, i)
            if cur_point == origin:
                print("s", end=" ")
            elif cur_point in covered_positions:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()


print("Advent of Code 2022 Day 9")
print("-------------------------")
# file_input = io.file_to_list("input/day-9-test-data.txt")
file_input = io.file_to_list("input/day-9-test-data-2.txt")
# file_input = io.file_to_list("input/day-9-input.txt")
rope_head_moves = []

for line in file_input:
    rope_head_moves.append(line.split(" "))

head_position = Point2D(0, 0)
last_updated_knot = Point2D(0, 0)   # Tail starts out overlapped by head.
covered_positions = []
# max_x = 0
# max_y = 0
for move in rope_head_moves:
    direction = move[0]
    num_steps = int(move[1])
    # max_x = num_steps if direction == "U" and num_steps > max_x else max_x
    # max_y = num_steps if direction == "R" and num_steps > max_y else max_y

    for i in range(num_steps):
        head_position, last_updated_knot = calculate_moves(head_position=head_position, tail_position=last_updated_knot, direction=direction)
        if last_updated_knot not in covered_positions:
            covered_positions.append(Point2D(last_updated_knot.x, last_updated_knot.y))

if last_updated_knot not in covered_positions:
    covered_positions.append(last_updated_knot) # Count the tail's position once the loop ends.

# print(f"covered_positions (final): {covered_positions}")
# print(f"max_x: {max_x}")
# print(f"max_y: {max_y}")
# Print human-readable version of covered_positions.
# print_tail_positions(max_x, max_y, covered_positions)

num_tail_positions_visited = len(covered_positions)
print("PART 1")
print("======")
print(f"Number of distinct positions visited by rope tail: {num_tail_positions_visited}")
print("======")
# Attempt 1: 8986 (too high)
# Attempt 2: 6266

# max_x = 0
# max_y = 0
covered_positions.clear()
rope_knots = [Point2D(0, 0) for i in range(10)] # Make a ten-knot rope.
last_updated_knot = Point2D(rope_knots[0].x, rope_knots[0].y)    # Final element is tail of rope.
tail_index = len(rope_knots) - 1
for move in rope_head_moves:
    print(f"move: {' '.join(move)}")
    direction = move[0]
    num_steps = int(move[1])
    print(f"num_steps: {num_steps}")
    # max_x = num_steps if direction == "U" and num_steps > max_x else max_x
    # max_y = num_steps if direction == "R" and num_steps > max_y else max_y
    extra_loop = num_steps >= len(rope_knots)
    for i in range(num_steps):
        print(f"Step {i + 1} of {num_steps}.")
        j = 0
        while j <= i:   # If the head moves n steps, the next n knots move in sequence.
            print(f"j: {j}")
            print(f"rope_knots (before move): {rope_knots}")
            if j + 1 > tail_index and extra_loop:
                print(f"Reached end of rope.")
                # Reached end of the rope, but the head still needs to move a few more steps.
                num_steps -= j + 1
                break
            cur_head = rope_knots[j]
            cur_tail = rope_knots[j + 1]
            # print(f"rope_knots before move: {rope_knots}")
            print(f"Head before move ({j}): {cur_head}")
            print(f"Tail before move ({j + 1}): {cur_tail}")
            cur_head, cur_tail = calculate_moves(head_position=cur_head, tail_position=cur_tail, direction=direction)
            # rope_knots[j] = cur_head
            # rope_knots[j + 1] = cur_tail
            last_updated_knot = Point2D(cur_tail.x, cur_tail.y)
            # print(f"rope_knots after move: {rope_knots}")
            print(f"Head after move ({j}): {cur_head}")
            print(f"Tail after move ({j + 1}): {cur_tail}")
            print(f"rope_knots (after move): {rope_knots}")

            if j + 1 == tail_index and cur_tail not in covered_positions:
                print(f"Recording tail position: {cur_tail}")
                # cur_tail is the tail of the rope; record its current position if new.
                covered_positions.append(Point2D(cur_tail.x, cur_tail.y))

            j += 1
            print()

    if extra_loop:
        print("Reached end of rope. Now moving all knots.")
        print(f"Steps left: {num_steps}")
        for i in range(num_steps):
            print(f"Step {i + 1} of {num_steps}.")
            # Move entire rope however many steps left the head has to take.
            cur_head, cur_tail = calculate_moves(head_position=cur_head, tail_position=cur_tail, direction=direction)
            last_updated_knot = Point2D(cur_tail.x, cur_tail.y)
    print(f"rope_knots (after executing move instruction): {rope_knots}")

if last_updated_knot not in covered_positions:
    covered_positions.append(last_updated_knot) # Count the tail's position once the loop ends.

print(f"covered_positions (final): {covered_positions}")
num_tail_positions_visited = len(covered_positions)
print("PART 2")
print("======")
print(f"Number of distinct positions visited by rope tail: {num_tail_positions_visited}")
print("======")
# Attempt 1: 1106 (too low)
# Attempt 2: 1834 (too low)
