from lib import io
from lib.collections import DirectedGraph, Vertex

print("Advent of Code 2022 Day 12")
print("-------------------------")

testing = False
if testing:
    height_map_string = io.file_to_string("input/day-12-test-data.txt")
    height_map = io.file_to_list("input/day-12-test-data.txt")
    num_rows, num_cols = io.file_dimensions("input/day-12-test-data.txt")
else:
    height_map_string = io.file_to_string("input/day-12-input.txt")
    height_map = io.file_to_list("input/day-12-input.txt")
    num_rows, num_cols = io.file_dimensions("input/day-12-input.txt")
# print(f"File dimensions: {num_rows}, {num_cols}")

def is_traversable(start_char, end_char):
    # print("In is_traversable().")
    # print(f"start_char: {start_char}")
    # print(f"end_char: {end_char}")
    # Convert the starting and ending point characters to their heights first.
    if start_char == "S":
        start_char = "a"
        # print(f"start_char (after conversion): {start_char}")
    elif start_char == "E":
        start_char = "z"
        # print(f"start_char (after conversion): {start_char}")

    if end_char == "S":
        end_char = "a"
        # print(f"end_char (after conversion): {end_char}")
    elif end_char == "E":
        end_char = "z"
        # print(f"end_char (after conversion): {end_char}")
    # print("Exiting is_traversable().")
    # return ord(end_char) - ord(start_char) <= 1 # End must be at most 1 unit higher than start.
    height_difference = ord(end_char) - ord(start_char)
    if abs(height_difference) <= 1:
        return 1    # Can go in both directions between start and end.
    elif height_difference < 0:
        return 0    # Can only go from start to end.
    else:
        return -1   # Not possible to go from start to end.

def connect_squares(graph, starting_square, ending_square):
    # print("In connect_squares().")
    if ending_square:
        ending_square = graph.add_vertex(ending_square)
        edge_type = is_traversable(starting_square.data, ending_square.data)
        if edge_type == 1:
            # Connect starting_square and ending_square in both directions.
            status = graph.add_edge(starting_square, ending_square)
            # if status:
            #     print(f"Made edge from {starting_square} to {ending_square}.")
            # else:
            #     print(f"Failed to make edge from {starting_square} to {ending_square}.")
            status = graph.add_edge(ending_square, starting_square)
            # if status:
            #     print(f"Made edge from {ending_square} to {starting_square}.")
            # else:
            #     print(f"Failed to make edge from {ending_square} to {starting_square}")
        elif edge_type == 0:
            # Only connect starting_square to ending_square.
            status = graph.add_edge(starting_square, ending_square)
            # if status:
            #     print(f"Made edge from {starting_square} to {ending_square}.")
            # else:
            #     print(f"Failed to make edge from {starting_square} to {ending_square}.")
        elif edge_type == -1:
            pass

    # print("Exiting connect_squares().\n")

# Construct graph representing all connected grid squares.
accessible_areas = DirectedGraph()
for i in range(len(height_map)):
    for j in range(len(height_map[i])):
        # print(f"i: {i}")
        # print(f"j: {j}")
        # print(f"height_map[{i}][{j}]: {height_map[i][j]}")
        cur_square = Vertex(num_cols * i + j, height_map[i][j])
        # print(f"cur_square: {cur_square}")
        cur_square = accessible_areas.add_vertex(cur_square)

        # Check each of height_map[i][j]'s neighbours.
        # If neighbour is accessible, add it to the graph.
        northern_label = num_cols * (i - 1) + j
        northern_neighbour = Vertex(
            northern_label,
            height_map[i - 1][j]
        ) if i - 1 >= 0 else None
        southern_label = num_cols * (i + 1) + j
        southern_neighbour = Vertex(
            southern_label,
            height_map[i + 1][j]
        ) if i + 1 < len(height_map) else None
        eastern_label = num_cols * i + (j + 1)
        eastern_neighbour = Vertex(
            eastern_label,
            height_map[i][j + 1]
        ) if j + 1 < len(height_map[i]) else None
        western_label = num_cols * i + (j - 1)
        western_neighbour = Vertex(
            western_label,
            height_map[i][j - 1]
        ) if j - 1 >= 0 else None

        connect_squares(accessible_areas, cur_square, northern_neighbour)
        connect_squares(accessible_areas, cur_square, southern_neighbour)
        connect_squares(accessible_areas, cur_square, eastern_neighbour)
        connect_squares(accessible_areas, cur_square, western_neighbour)

# print("accessible_areas:")
# print(accessible_areas)

# Run shortest path algorithm on graph from S to E.
current_position = accessible_areas.get_vertex(height_map_string.replace("\n", "").find("S"))
destination = accessible_areas.get_vertex(height_map_string.replace("\n", "").find("E"))
# print(f"\ncurrent_position (before search): {current_position}")
# print(f"destination (before search): {destination}")
accessible_areas.bfs(current_position)
# path = []
# accessible_areas.get_path(current_position, destination, path)
# print(f"\ncurrent_position (after search): {current_position}")
# print(f"destination (after search): {destination}")
# print(f"path: {path}")
print("PART 1")
print("======")
print(f"Shortest number of steps from current position to destination: {destination.distance}")
print("======")
# Attempt 1: 423
