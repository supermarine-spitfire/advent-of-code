from enum import Enum

from lib import io
from lib.geometry import LineSegment2D, Point2D

class Direction(Enum):
    BLOCKED = -1
    DOWN = 0
    LEFT = 1
    RIGHT = 2

def free_to_move(sand, walls, placed_sand):
    def is_free(point):
        # Check if point hits a wall or placed sand.
        if point in walls or point in placed_sand:
            return False
        else:
            return True

    # First check if the point directly down is free.
    # If not free, check down left then down right.
    # If no place is free, sand cannot move.
    if is_free(Point2D(sand.x, sand.y + 1)):
        return Direction.DOWN
    elif is_free(Point2D(sand.x - 1, sand.y + 1)):
        return Direction.LEFT
    elif is_free(Point2D(sand.x + 1, sand.y + 1)):
        return Direction.RIGHT
    else:
        return Direction.BLOCKED

testing = False
if testing:
    cave_scan = io.file_to_list("input/day-14-test-data.txt")
else:
    cave_scan = io.file_to_list("input/day-14-input.txt")

print("Advent of Code 2022 Day 14")
print("-------------------------")

# Construct a model of the cave given input. Said input defines the walls and floors (henceforth "wall"), through which sand cannot penetrate.
max_y = 0   # Tracks the lowest cave wall in system. Sand that goes below this will fall for ever.
cave_walls = set()
for line in cave_scan:
    # Each line defines a contiguous cave wall.
    # cave_wall = []
    segments = line.split("->")
    for i in range(len(segments) - 1):
        start_x, start_y = segments[i].split(",")
        end_x, end_y = segments[i + 1].split(",")
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)

        if start_x == end_x:    # Vertical segment.
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                # print(f"Point: ({start_x}, {y})")
                cave_walls.add(Point2D(start_x, y))
        else:                   # Horizontal segment.
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                # print(f"Point: ({x}, {start_y})")
                cave_walls.add(Point2D(x, start_y))

        max_y = start_y if start_y > max_y else max_y
        max_y = end_y if end_y > max_y else max_y
# print(f"max_y: {max_y}")

# Start pouring sand from point (500, 0).
# Loop as long as a unit of sand can come to a rest.
can_rest = True
placed_sand_units = set()
while can_rest:
    sand = Point2D(500, 0)
    direction = Direction.DOWN
    while direction != Direction.BLOCKED:
        direction = free_to_move(sand, cave_walls, placed_sand_units)
        # print(f"direction: {direction}")
        if direction == Direction.DOWN:
            sand.y += 1
        elif direction == Direction.LEFT:
            sand.x -= 1
            sand.y += 1
        elif direction == Direction.RIGHT:
            sand.x += 1
            sand.y += 1

        # print(f"sand.y: {sand.y}")
        if sand.y > max_y:
            # Sand is falling into the abyss; terminate.
            can_rest = False
            break

    if can_rest:
        placed_sand_units.add(sand)

print("PART 1")
print("======")
print(f"Maximum number of sand units deposited before excess flows over: {len(placed_sand_units)}")
print("======")
# Attempt 1: 698
# Time trial 1: 52.2 s
# Time trial 2: 0.4 s
