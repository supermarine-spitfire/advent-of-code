from enum import Enum

from lib import io
from lib.geometry import Line2D, Point2D

class Direction(Enum):
    BLOCKED = -1
    DOWN = 0
    LEFT = 1
    RIGHT = 2

def free_to_move(sand, walls, placed_sand):
    def is_free(point):
        # Check if it hits a wall.
        for wall in walls:
            if wall.intersects(point):
                return False

        # Check if it hits placed sand.
        for ps in placed_sand:
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

testing = False
if testing:
    cave_scan = io.file_to_list("input/day-14-test-data.txt")
else:
    cave_scan = io.file_to_list("input/day-14-input.txt")

print("Advent of Code 2022 Day 14")
print("-------------------------")

# Construct a model of the cave given input. Said input defines the walls and floors (henceforth "wall"), through which sand cannot penetrate.
cave_walls = []
for line in cave_scan:
    # Each line defines a contiguous cave wall.
    # cave_wall = []
    segments = line.split("->")
    for i in range(len(segments) - 1):
        start = segments[i].split(",")
        end = segments[i + 1].split(",")
        wall_segment = Line2D(
            start=Point2D(int(start[0]), int(start[1])),
            end=Point2D(int(end[0]), int(end[1])),
        )
        cave_walls.append(wall_segment)
        # cave_wall.append(wall_segment)
    # cave_walls.append(cave_wall)

# Start pouring sand from point (500, 0).
# Loop as long as a unit of sand can come to a rest.
can_rest = True
placed_sand_units = []
while True:
    sand = Point2D(500, 0)
    direction = free_to_move(sand, cave_walls, placed_sand_units)
    while direction != Direction.BLOCKED:
        direction = free_to_move(sand, cave_walls, placed_sand_units)
        if direction == Direction.DOWN:
            pass
        elif direction == Direction.LEFT:
            pass
        elif direction == Direction.RIGHT:
            pass

print("PART 1")
print("======")
print(f"Maximum number of sand units deposited before excess flows over:")
print("======")
