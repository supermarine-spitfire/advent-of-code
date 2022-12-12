from lib import io
from lib.collections import Graph, Vertex

print("Advent of Code 2022 Day 12")
print("-------------------------")

height_map_string = io.file_to_string("input/day-12-test-data.txt")
height_map = io.file_to_list("input/day-12-test-data.txt")
num_height_map_rows, num_height_map_cols = io.file_dimensions("input/day-12-test-data.txt")

def is_traversable(start_char, end_char):
    # Convert the starting and ending point characters to their heights first.
    if start_char == "S":
        start_char = "a"
    elif start_char == "E":
        start_char = "z"

    if end_char == "S":
        end_char = "a"
    elif end_char == "E":
        end_char = "z"
    return ord(end_char) - ord(start_char) <= 1

def connect_squares(graph, starting_square, ending_square):
    if ending_square and is_traversable(starting_square.data, ending_square.data):
        graph.add_vertex(ending_square)
        graph.add_edge(starting_square, ending_square)

# Construct graph representing all connected grid squares.
accessible_areas = Graph()
for i in range(len(height_map)):
    for j in range(len(height_map[i])):
        # print(f"i: {i}")
        # print(f"j: {j}")
        print(f"height_map[{i}][{j}]: {height_map[i][j]}")
        cur_square = Vertex(num_height_map_rows * i + j, height_map[i][j])
        print(f"cur_square: {cur_square}")
        accessible_areas.add_vertex(cur_square)

        # Check each of height_map[i][j]'s neighbours.
        # If neighbour is accessible, add it to the graph.
        northern_neighbour = Vertex(
            num_height_map_rows * (i - 1) + j,
            height_map[i - 1][j]
        ) if i - 1 >= 0 else None
        southern_neighbour = Vertex(
            num_height_map_rows * (i + 1) + j,
            height_map[i + 1][j]
        ) if i + 1 < len(height_map) else None
        eastern_neighbour = Vertex(
            num_height_map_rows * i + (j + 1),
            height_map[i][j + 1]
        ) if j + 1 < len(height_map[i]) else None
        western_neighbour = Vertex(
            num_height_map_rows * i + (j - 1),
            height_map[i][j - 1]
        ) if j - 1 >= 0 else None

        # print(f"northern_neighbour: {northern_neighbour}")
        # print(f"southern_neighbour: {southern_neighbour}")
        # print(f"eastern_neighbour: {eastern_neighbour}")
        # print(f"western_neighbour: {western_neighbour}")
        # print()

        connect_squares(accessible_areas, cur_square, northern_neighbour)
        connect_squares(accessible_areas, cur_square, southern_neighbour)
        connect_squares(accessible_areas, cur_square, eastern_neighbour)
        connect_squares(accessible_areas, cur_square, western_neighbour)

print("accessible_areas:")
print(accessible_areas)

# Run shortest path algorithm on graph from S to E.
current_position = accessible_areas.get_vertex(height_map_string.replace("\n", "").find("S"))
destination = accessible_areas.get_vertex(height_map_string.replace("\n", "").find("E"))
print(f"current_position: {current_position}")
print(f"destination: {destination}")
accessible_areas.bfs(current_position)
