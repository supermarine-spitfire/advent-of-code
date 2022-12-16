import re, sys

from functools import reduce
from itertools import combinations

from lib import io
from lib.geometry import Point2D, LineSegment2D

class Sensor:
    def __init__(self, location, closest_beacon):
        self.location = location
        self.closest_beacon = closest_beacon

        self.sensor_range = location.manhattan_distance(closest_beacon)

    def __str__(self):
        return f"""Location: {self.location}
Closest beacon: {self.closest_beacon} ({self.sensor_range} units away)
"""

    __repr__ = __str__

    def __hash__(self):
        return hash((self.location, self.closest_beacon))

    def __eq__(self, other):
        if isinstance(other, Sensor):
            return self.location == other.location and self.closest_beacon == other.closest_beacon
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_in_range(self, p):
        return self.location.manhattan_distance(p) <= self.sensor_range

    def get_detectable_points(self):
        detectable_points = set()
        # Sensor area consists of two triangles with their bases touching.
        # Go from base to tip in each loop.
        # print("Making top half of range.")
        # print(f"self.sensor_range - 1: {self.sensor_range - 1}")
        # print(f"self.location.y - self.sensor_range - 1: {self.location.y - self.sensor_range - 1}")
        row = self.sensor_range - 1
        while row < self.location.y - self.sensor_range - 1:
            col = self.location.x - self.sensor_range - row
            while col < self.location.x + self.sensor_range + row + 1:
                # print(f"({row}, {col})")
                detectable_points.add(Point2D(row, col))
                col += 1
            row += 1
        # print("Making dividing line of range.")
        row = self.location.x - self.sensor_range
        while row < self.location.x + self.sensor_range + 1:
            # print(f"({row}, {self.location.y})")
            # Construct dividing line of range.
            detectable_points.add(Point2D(row, self.location.y))
            row += 1
        # print("Making bottom half of range.")
        # print(f"self.sensor_range + 1: {self.sensor_range + 1}")
        # print(f"self.location.y + self.sensor_range + 1: {self.location.y + self.sensor_range + 1}")
        row = self.sensor_range + 1
        while row < self.location.y + self.sensor_range + 1:
            col = self.location.x - self.sensor_range - row
            while col < self.location.x + self.sensor_range + row + 1:
                # print(f"({row}, {col})")
                detectable_points.add(Point2D(row, col))
                col += 1
            row += 1

        return detectable_points

testing = True
if testing:
    beacon_sensor_data = io.file_to_list("input/day-15-test-data.txt")
    row_to_search = 10
else:
    beacon_sensor_data = io.file_to_list("input/day-15-input.txt")
    row_to_search = 2000000

print("Advent of Code 2022 Day 15")
print("-------------------------")

# Extract sensor and beacon data.
sensors = []
coord_pair_ptrn = re.compile(r"x=-?\d+, y=-?\d+")
coord_ptrn = re.compile(r"-?\d+")
min_x = sys.maxsize
max_x = 0
# min_y = sys.maxsize
# max_y = 0
for line in beacon_sensor_data:
    # print(f"line: {line}")
    coords = coord_pair_ptrn.findall(line)
    sensor_coords = tuple(map(lambda x: int(x), coord_ptrn.findall(coords[0])))
    beacon_coords = tuple(map(lambda x: int(x), coord_ptrn.findall(coords[1])))
    x = min(sensor_coords[0], beacon_coords[0])
    y = min(sensor_coords[1], beacon_coords[1])

    min_x = min(beacon_coords[0], min_x)
    max_x = max(beacon_coords[0], max_x)
    # min_x = min(sensor_coords[0], beacon_coords[0]) if x < min_x else min_x
    # min_y = min(sensor_coords[1], beacon_coords[1]) if y < min_y else min_y
    # max_x = max(sensor_coords[0], beacon_coords[0]) if x > max_x else max_x
    # max_y = max(sensor_coords[1], beacon_coords[1]) if y > max_y else max_y

    sensors.append(
        Sensor(
            location=Point2D(sensor_coords[0], sensor_coords[1]),
            closest_beacon=Point2D(beacon_coords[0], beacon_coords[1])
        )
    )

# for s in sensors:
#     print("\nCurrent sensor:")
#     print(s)
#     s.get_detectable_points()
max_sensor_range = reduce(lambda s, t: s if s.sensor_range > t.sensor_range else t, sensors).sensor_range

# In the row row_to_search, figure out which positions are covered by sensors' detection range.
# Two possible approaches:
# 1. For each position in row_to_search, only include those that fall within a sensor's range.
#    Run the previous instruction for each sensor.
#    From those points, remove those that are occupied by a sensor or a beacon.
# 2. For each sensor, define a set of all positions that are within range (<= Manhattan distance to beacon).
#    Intersect all those sets, along with a set of the positions in row_to_search.
#    From those points, remove those that are occupied by a sensor or a beacon.
# print(f"row_to_search: {row_to_search}")
# print(f"min_x: {min_x}")
# print(f"max_x: {max_x}")
# Approach 1.
positions = set()
for x in range(min_x - max_sensor_range, max_x + max_sensor_range + 1):
    p = Point2D(x, row_to_search)
    for s in sensors:
        if s.is_in_range(p):
            positions.add(p)
            # break   # No need to consider any more sensors.

# Approach 2.


# positions -= {s.location for s in sensors}          # Remove any positions occupied by a sensor.
positions -= {s.closest_beacon for s in sensors}    # Remove any positions occupied by a beacon.

print("PART 1")
print("======")
print(f"Number of positions not occupied by a beacon at y = {row_to_search}: {len(positions)}")
print("======")
# Attempt 1: 5567803 (too low; 36.8 s)
# Attempt 2: 6275922

# To capture the point at which the distress beacon is located, use the following insight:
# The beacon can be found by considering the minimum distance from each sensor at which a
# beacon can be overlooked. This distance is one unit greater than the saved Manhattan distance
# to the closest discovered beacon to the sensor.
# Algorithm is as follows:
# Expand each sensor's range by 1. Construct the boundaries of this region.
# Identify the intersection point of four of these ranges.
# This point is the location of the distress beacon.
sensor_borders = {} # Model each sensor's range as a square.
for s in sensors:
    # Construct the corners of the square.
    min_undetected_distance = s.sensor_range + 1

    top = Point2D(s.location.x, s.location.y - min_undetected_distance)
    bottom = Point2D(s.location.x, s.location.y + min_undetected_distance)
    left = Point2D(s.location.x - min_undetected_distance, s.location.y)
    right = Point2D(s.location.x + min_undetected_distance, s.location.y)

    # Construct square sides.
    sides = [LineSegment2D(top, right), LineSegment2D(right, bottom), LineSegment2D(bottom, left), LineSegment2D(left, top)]
    sensor_borders[s] = sides

# print(f"sensor_borders: {sensor_borders}")
# Go through sensor_borders in groups of size 4.
# In each group, check if there are four sides that intersect, one from each sensor border region.
groups_of_4 = list(combinations(sensors, 4))
print(f"groups_of_4 ({len(groups_of_4)}):")
intersecting_sides = None
for g in groups_of_4:
    # print(g)
    sides = sensor_borders[g[0]] + sensor_borders[g[1]] + sensor_borders[g[2]] + sensor_borders[g[3]]
    print(f"sides: {sides}")
    side_groups = list(combinations(sides, 4))
    for side_group in side_groups:
        s1 = side_group[0]
        s2 = side_group[1]
        s3 = side_group[2]
        s4 = side_group[3]
        if s1.intersects_line_segment(s2) and s2.intersects_line_segment(s3) and s3.intersects_line_segment(s4) and s4.intersects_line_segment(s1):
            intersecting_sides = side_group
            break

print(f"intersecting_sides: {intersecting_sides}")

distress_beacon_x = 0
distress_beacon_y = 0

tuning_frequency = distress_beacon_x * 4000000 + distress_beacon_y
print("PART 2")
print("======")
print(f"Tuning frequency of beacon at ({distress_beacon_x}, {distress_beacon_y}): {tuning_frequency}")
print("======")