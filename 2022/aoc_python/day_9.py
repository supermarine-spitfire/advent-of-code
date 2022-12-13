from math import sqrt
from lib import io

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


def calculate_moves(head_position, tail_position, direction, use_old_implementation):
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
    elif direction == "LU":
        head_position.x -= 1
        head_position.y += 1
        # print(f"Moving head up and to the left: {head_position}")
    elif direction == "RU":
        head_position.x += 1
        head_position.y += 1
        # print(f"Moving head up and to the right: {head_position}")
    elif direction == "LD":
        head_position.x -= 1
        head_position.y -= 1
        # print(f"Moving head down and to the left: {head_position}")
    elif direction == "RD":
        head_position.x += 1
        head_position.y -= 1
        # print(f"Moving head up and to the right: {head_position}")
    else:
        pass    # Ignore any other input.

    # print(f"Tail position: {tail_position}")
    print(f"Previous head position: {previous_head_position}")
    print()
    if use_old_implementation:
        # This is the old implementation which updates the head and tail at once.
        # Keep for Part 1 until the new one is confirmed to work.
        print("Using old implementation.")
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
    else:
        if not tail_position:   # Used for when tail's movement is not needed.
            return None
        # This is the new implementation that only moves the head.
        # It will calculate and return the direction the tail should go and how many steps it should take.
        print("Using new implementation.")
        print(f"head_position: {head_position}")
        print(f"tail_position: {tail_position}")
        if head_position.euclidean_distance(tail_position) == 2:
            print("Move tail horizontally/vertically.")
           # Horizontal/vertical moves.
            if head_position.x == tail_position.x:
                # Do a vertical move.
                if head_position.y > tail_position.y:
                    return "U"
                elif head_position.y <  tail_position.y:
                    return "D"
            elif head_position.y == tail_position.y:
                # Do a horizontal move.
                if head_position.x > tail_position.x:
                    return "R"
                elif head_position.x <  tail_position.x:
                    return "L"

            return "N", 0   # A null move; should not happen.
        elif head_position.euclidean_distance(tail_position) > 2:
            print("Move tail diagonally.")
            # Diagonal moves.
            # Cases:
            # 1. Left-up.
            # 2. Right-up.
            # 3. Left-down.
            # 4. Right-down.
            if head_position.y > tail_position.y:
                if head_position.x > tail_position.x:
                    # Do right-up move.
                    return "RU"
                elif head_position.x < tail_position.x:
                    # Do left-up move.
                    return "LU"
            elif head_position.y < tail_position.y:
                if head_position.x > tail_position.x:
                    # Do right-down move.
                    return "RD"
                elif head_position.x < tail_position.x:
                    # Do left-down move.
                    return "LD"

            return "N", 0   # A null move; should not happen.
        print("No tail movement.")
        return "N"   # A null move; should not happen.


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
# file_input = io.file_to_list("input/day-9-test-data-2.txt")
file_input = io.file_to_list("input/day-9-input.txt")
rope_head_moves = []

for line in file_input:
    rope_head_moves.append(line.split(" "))

head_position = Point2D(0, 0)
tail_position = Point2D(0, 0)   # Tail starts out overlapped by head.
covered_positions = []
# max_x = 0
# max_y = 0
for move in rope_head_moves:
    direction = move[0]
    num_steps = int(move[1])
    # max_x = num_steps if direction == "U" and num_steps > max_x else max_x
    # max_y = num_steps if direction == "R" and num_steps > max_y else max_y

    for i in range(num_steps):
        # head_position, tail_position = calculate_moves(
        #     head_position=head_position,
        #     tail_position=tail_position,
        #     direction=direction,
        #     use_old_implementation=True
        # )
        # if tail_position not in covered_positions:
        #     covered_positions.append(Point2D(tail_position.x, tail_position.y))
        # Move head.
        direction = calculate_moves(
            head_position=head_position,
            tail_position=tail_position,
            direction=direction,
            use_old_implementation=False
        )
        # Move tail.
        calculate_moves(
            head_position=tail_position,
            tail_position=None,
            direction=direction,
            use_old_implementation=False
        )

        if tail_position not in covered_positions:
            covered_positions.append(tail_position) # Count the tail's position once the loop ends.

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
for move in rope_head_moves:
    print(f"move: {' '.join(move)}")
    num_steps = int(move[1])
    print(f"num_steps: {num_steps}")
    for num_step in range(num_steps):
        print(f"rope_knots: {rope_knots}")
        direction = move[0]
        for i in range(len(rope_knots) - 1):
            rel_head = rope_knots[i]
            rel_tail = rope_knots[i + 1]
            direction = calculate_moves(
                head_position=rel_head,
                tail_position=rel_tail,
                direction=direction,
                use_old_implementation=False
            )
        # Move final element in rope_knots.
        # Do not really care about the return value at this point.
        calculate_moves(
            head_position=rope_knots[-1],
            tail_position=None,
            direction=direction,
            use_old_implementation=False
        )
        if rope_knots[-1] not in covered_positions:
            covered_positions.append(Point2D(rel_tail.x, rel_tail.y))
    print(f"covered_positions (after executing move instruction {' '.join(move)}): {covered_positions}")

print(f"covered_positions (final): {covered_positions}")
num_tail_positions_visited = len(covered_positions)
print("PART 2")
print("======")
print(f"Number of distinct positions visited by rope tail: {num_tail_positions_visited}")
print("======")
# Attempt 1: 1106 (too low)
# Attempt 2: 1834 (too low)
# Attempt 3: 2369
