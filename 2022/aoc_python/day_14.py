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
        print("In is_free().")
        print(f"point: {point}")
        # Check if it hits a wall.
        for wall in walls:
            print(f"wall: {wall}")
            if wall.intersects(point):
                return False

        # Check if it hits placed sand.
        for ps in placed_sand:
            print(f"ps: {ps}")
            if ps.is_touching(point):
                False
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

testing = True
if testing:
    cave_scan = io.file_to_list("input/day-14-test-data.txt")
else:
    cave_scan = io.file_to_list("input/day-14-input.txt")

print("Advent of Code 2022 Day 14")
print("-------------------------")

# Construct a model of the cave given input. Said input defines the walls and floors (henceforth "wall"), through which sand cannot penetrate.
max_y = 0   # Tracks the lowest cave wall in system. Sand that goes below this will fall for ever.
cave_walls = []
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
        wall_segment = LineSegment2D(
            start=Point2D(start_x, start_y),
            end=Point2D(end_x, end_y),
        )
        max_y = start_y if start_y > max_y else max_y
        max_y = end_y if end_y > max_y else max_y
        cave_walls.append(wall_segment)
        # cave_wall.append(wall_segment)
    # cave_walls.append(cave_wall)
print(f"max_y: {max_y}")

# Start pouring sand from point (500, 0).
# Loop as long as a unit of sand can come to a rest.
can_rest = True
placed_sand_units = []
while can_rest:
    sand = Point2D(500, 0)
    direction = Direction.DOWN
    while direction != Direction.BLOCKED:
        direction = free_to_move(sand, cave_walls, placed_sand_units)
        print(f"direction: {direction}")
        if direction == Direction.DOWN:
            sand.y += 1
        elif direction == Direction.LEFT:
            sand.x -= 1
            sand.y += 1
        elif direction == Direction.RIGHT:
            sand.x += 1
            sand.y += 1

        print(f"sand.y: {sand.y}")
        if sand.y > max_y:
            # Sand is falling into the abyss; terminate.
            can_rest = False

    if can_rest:
        placed_sand_units.append(sand)

print("PART 1")
print("======")
print(f"Maximum number of sand units deposited before excess flows over: {len(placed_sand_units)}")
print("======")
