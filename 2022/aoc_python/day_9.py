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

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self):
        return f"Point2D({self.x}, {self.y})"

    __repr__ = __str__


print("Advent of Code 2022 Day 9")
print("-------------------------")
file_input = io.file_to_list("input/day-9-test-data.txt")
# file_input = io.file_to_list("input/day-9-input.txt")
rope_head_moves = []

for line in file_input:
    rope_head_moves.append(line.split(" "))

origin = Point2D(0, 0)          # Map everything relative to this point.
head_position = Point2D(0, 0)
tail_position = Point2D(0, 0)   # Tail starts out overlapped by head.
covered_positions = []
for move in rope_head_moves:
    print(f"covered_positions: {covered_positions}")
    direction = move[0]
    num_steps = int(move[1])

    # Move the head.
    if direction == "U":
        # Moving up.
        for i in range(num_steps):
            head_position.y += 1
            print(f"Moving head up: {head_position}")
            if head_position.x == tail_position.x:
                # Tail is directly above/below head.
                # If statement checks if head and tail are touching or not.
                if head_position.euclidean_distance(tail_position) >= 2:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    tail_position.y += 1
                    print(f"Moving tail up: {tail_position}")
            elif head_position.y > tail_position.y:
                # Tail is on a downward diagonal relative to head.
                # If statement checks if head and tail are touching or not.
                if head_position.manhattan_distance(tail_position) >= 3:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    # Tail occupies original position of head.
                    tail_position.x = head_position.x
                    tail_position.y = head_position.y - 1
                    print(f"Moving tail diagonally up to previous position of head: {tail_position}")
            # Other possible tail positions (side-by-side with head, on upward diagonal relative to head)
            # do not warrant updating its position.
    elif direction == "D":
        # Moving down.
        for i in range(num_steps):
            head_position.y -= 1
            print(f"Moving head down: {head_position}")
            if head_position.x == tail_position.x:
                # Tail is directly above/below head.
                # If statement checks if head and tail are touching or not.
                if head_position.euclidean_distance(tail_position) >= 2:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    tail_position.y -= 1
                    print(f"Moving tail down: {tail_position}")
            elif head_position.y < tail_position.y:
                # Tail is on an upward diagonal relative to head.
                # If statement checks if head and tail are touching or not.
                if head_position.manhattan_distance(tail_position) >= 3:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    # Tail occupies original position of head.
                    tail_position.x = head_position.x
                    tail_position.y = head_position.y + 1
                    print(f"Moving tail diagonally down to previous position of head: {tail_position}")
            # Other possible tail positions (side-by-side with head, on downward diagonal relative to head)
            # do not warrant updating its position.
    elif direction == "L":
        # Moving left.
        for i in range(num_steps):
            head_position.x -= 1
            print(f"Moving head left: {head_position}")
            if head_position.y == tail_position.y:
                # Tail is side-by-side with head.
                # If statement checks if head and tail are touching or not.
                if head_position.euclidean_distance(tail_position) >= 2:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    tail_position.x -= 1
                    print(f"Moving tail left: {tail_position}")
            elif head_position.x < tail_position.x:
                # Tail is on a rightward diagonal relative to head.
                # If statement checks if head and tail are touching or not.
                if head_position.manhattan_distance(tail_position) >= 3:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    # Tail occupies original position of head.
                    tail_position.y = head_position.y
                    tail_position.x = head_position.x + 1
                    print(f"Moving tail diagonally up to previous position of head: {tail_position}")
            # Other possible tail positions (above/below head, on leftward diagonal relative to head)
            # do not warrant updating its position.
    elif direction == "R":
        # Moving right.
        for i in range(num_steps):
            head_position.x += 1
            print(f"Moving head right: {head_position}")
            if head_position.y == tail_position.y:
                # Tail is side-by-side with head.
                # If statement checks if head and tail are touching or not.
                if head_position.euclidean_distance(tail_position) >= 2:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    tail_position.x += 1
                    print(f"Moving tail right: {tail_position}")
            elif head_position.x > tail_position.x:
                # Tail is on a leftward diagonal relative to head.
                # If statement checks if head and tail are touching or not.
                if head_position.manhattan_distance(tail_position) >= 3:
                    covered_positions.append(Point2D(tail_position.x, tail_position.y))
                    # Tail occupies original position of head.
                    tail_position.y = head_position.y
                    tail_position.x = head_position.x - 1
                    print(f"Moving tail diagonally up to previous position of head: {tail_position}")
            # Other possible tail positions (above/below head, on rightward diagonal relative to head)
            # do not warrant updating its position.
    else:
        continue    # Ignore any other input.

num_tail_positions_visited = len(set(covered_positions))
# num_tail_positions_visited = len(covered_positions)
print("PART 1")
print("======")
print(f"Number of distinct positions visited by rope tail: {num_tail_positions_visited}")
print("======")
# Attempt 1: 8986 (too high)
# Attempt 2: 
