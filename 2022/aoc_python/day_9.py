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


class Vector2D:
    def __init__(self, start, end):
        self.start = Point2D(start.x, end.y)
        self.end = Point2D(end.x, end.y)

    def add(self, v):
        # Assumes vectors are defined using the same coordinate system.
        new_end = self.end.add(v.end.x, v.end.y)
        return Vector2D(self.start, new_end)

    def subtract(self, v):
        # Assumes vectors are defined using the same coordinate system.
        new_end = self.end.subtract(v.end.x, v.end.y)
        return Vector2D(self.start, new_end)

    def scalar_multiplication(self, c):
        scaled_vector = Vector2D(self.start.scale(c), self.end.scale(c))
        return scaled_vector

    def euclidean_distance(self) -> float:
        return sqrt(pow(self.end.x - self.start.x, 2) + pow(self.end.y - self.start.y, 2))

    def manhattan_distance(self) -> float:
        return abs(self.end.x - self.start.x, 2) + abs(self.end.y - self.start.y, 2)


print("Advent of Code 2022 Day 9")
print("-------------------------")
# file_input = io.file_to_list("input/day-9-test-data.txt")
file_input = io.file_to_list("input/day-9-input.txt")
rope_head_moves = []

for line in file_input:
    rope_head_moves.append(line.split(" "))

origin = Point2D(0, 0)          # Map everything relative to this point.
head_position = Point2D(0, 0)
tail_position = Point2D(0, 0)   # Tail starts out overlapped by head.
covered_positions = []
max_x = 0
max_y = 0
for move in rope_head_moves:
    # print(f"move: {move}")
    # print(f"covered_positions: {covered_positions}")
    # print(f"current head position: {head_position}")
    # print(f"current tail position: {tail_position}")
    direction = move[0]
    num_steps = int(move[1])
    max_x = num_steps if direction == "U" and num_steps > max_x else max_x
    max_y = num_steps if direction == "R" and num_steps > max_y else max_y

    for i in range(num_steps):
        # Move the head.
        previous_head_position = Point2D(head_position.x, head_position.y)
        if direction == "U":
            head_position.y += 1
            # print(f"Moving head up: {head_position}")
        elif direction == "D":
            head_position.y -= 1
            # print(f"Moving head down: {head_position}")
        elif direction == "L":
            head_position.x -= 1
            # print(f"Moving head left: {head_position}")
        elif direction == "R":
            head_position.x += 1
            # print(f"Moving head right: {head_position}")
        else:
            continue    # Ignore any other input.
        # print(f"Previous head position: {previous_head_position}")

        # Move the tail, if needed.
        # The distance checks test if head and tail are touching or not. Tail moves if the test fails.
        # The tail moves to the previous position of the head.
        if head_position.euclidean_distance(tail_position) >= 2  \
           or head_position.manhattan_distance(tail_position) >= 3:
           # Euclidean distance handles cases where head and tail are in same rows/columns.
           # Manhattan distance handles cases where head and tail are on diagonals.
           if tail_position not in covered_positions:
                covered_positions.append(Point2D(tail_position.x, tail_position.y))
           tail_position = previous_head_position
        #    print("Moving tail to previous head position.")
        #    print(f"New tail position: {tail_position}")
        #    print(f"covered_positions: {covered_positions}")
        # print()

if tail_position not in covered_positions:
    covered_positions.append(tail_position) # Count the tail's position once the loop ends.

print(f"covered_positions (final): {covered_positions}")
print(f"max_x: {max_x}")
print(f"max_y: {max_y}")
# Print human-readable version of covered_positions.
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

num_tail_positions_visited = len(covered_positions)
print("PART 1")
print("======")
print(f"Number of distinct positions visited by rope tail: {num_tail_positions_visited}")
print("======")
# Attempt 1: 8986 (too high)
# Attempt 2: 6266
