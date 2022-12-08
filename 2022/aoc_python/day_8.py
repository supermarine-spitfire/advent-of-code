from lib import io

def is_visible(tree_map, tree, const_index, start_index, end_index, const_row):
    # Assumes start_index is where the tree is; hence move up or down one as needed.
    if start_index > end_index: # Iterating backwards.
        r = range(start_index - 1, end_index, -1)
    else:                       # Iterating forwards.
        r = range(start_index + 1, end_index)

    for i in r:
        if const_row:   # Iterating across columns.
            if tree <= tree_map[const_index][i]:
                return False  # Already blocked from this angle.
        else:           # Iterating across rows.
            if tree <= tree_map[i][const_index]:
                return False  # Already blocked from this angle.

    return True


def viewing_distance(tree_map, tree, const_index, start_index, loop_forward, const_row):
    # print("In viewing_distance().")
    if const_row:
        # print("Moving east/west.")
        stop_index = len(tree_map[0]) - 1 if loop_forward else 0
    else:
        # print("Moving north/south.")
        stop_index = len(tree_map) - 1 if loop_forward else 0

    # print(f"const_index: {const_index}")
    # print(f"start_index: {start_index}")
    # print(f"stop_index: {stop_index}")
    distance = 0

    if loop_forward:    # Iterating forwards.
        i = start_index + 1 # Assumes start_index is where the tree is; hence move up or down one as needed.
        # print(f"i (before looping): {i}")
        # print("Moving forwards.")
        while i <= stop_index:
            # print(f"i: {i}")
            # print(f"Current distance: {distance}")
            if const_row:
                # print("Checking heights...")
                # print(f"Height being checked ({const_index}, {i}): {tree_map[const_index][i]}")
                distance += 1   # Include the tree that is taller or equal in height.
                if tree <= tree_map[const_index][i]:
                    break
            else:
                # print("Checking heights...")
                # print(f"Height being checked ({i}, {const_index}): {tree_map[i][const_index]}")
                distance += 1   # Include the tree that is taller or equal in height.
                if tree <= tree_map[i][const_index]:
                    break
            i += 1
    else:               # Iterating backwards.
        i = start_index - 1 # Assumes start_index is where the tree is; hence move up or down one as needed.
        # print(f"i (before looping): {i}")
        # print("Moving backwards.")
        while i >= stop_index:
            # print(f"i: {i}")
            # print(f"distance: {distance}")
            if const_row:
                # print("Checking heights...")
                # print(f"Height being checked ({const_index}, {i}): {tree_map[const_index][i]}")
                distance += 1   # Include the tree that is taller or equal in height.
                if tree <= tree_map[const_index][i]:
                    break
            else:
                # print("Checking heights...")
                # print(f"Height being checked ({i}, {const_index}): {tree_map[i][const_index]}")
                distance += 1   # Include the tree that is taller or equal in height.
                if tree <= tree_map[i][const_index]:
                    break
            i -= 1

    # print("Reached edge; returning.")
    # print(f"Final distance: {distance}")
    return distance


print("Advent of Code 2022 Day 8")
print("-------------------------")
tree_map_file = io.file_to_list("input/day-8-input.txt")
# tree_map_file = io.file_to_list("input/day-8-test-data.txt")
tree_map = []
for tree_row in tree_map_file:
    row = []
    for cur_tree in tree_row:
        row.append(int(cur_tree))
    tree_map.append(row)

max_scenic_score = 0

# First, calculate number of trees defining the border.
# General formula for the number of trees on the outside of an m x n grid is mn - (m - 2)(n - 2)
m = len(tree_map)       # Rows.
n = len(tree_map[0])    # Columns.
num_visible_trees = m * n - (m - 2) * (n - 2)
# print(f"Number of border trees: {num_visible_trees}")
# Now iterate over the enclosed trees.
for row_index in range(1, m - 1):
    cur_row = tree_map[row_index]
    for col_index in range(1, n - 1):
        # print(f"CURRENT COORDINATES: {row_index}, {col_index}")
        cur_tree = tree_map[row_index][col_index]
        # print(f"Current tree height: {cur_tree}")
        # Look northward (column is constant, row decrements).
        # print("\nLooking northward.")
        is_visible_north = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            end_index=-1,
            const_row=False
        )
        north_viewing_distance = viewing_distance(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            loop_forward=False,
            const_row=False
        )

        # Look southward (column is constant, row increments).
        # print("\nLooking southward.")
        is_visible_south = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            end_index=m,
            const_row=False
        )
        south_viewing_distance = viewing_distance(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            loop_forward=True,
            const_row=False
        )

        # Look westward (row is constant, column decrements).
        # print("\nLooking westward.")
        is_visible_west = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            end_index=-1,
            const_row=True
        )
        west_viewing_distance = viewing_distance(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            loop_forward=False,
            const_row=True
        )

        # Look eastward (row is constant, column increments).
        # print("\nLooking eastward.")
        is_visible_east = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            end_index=n,
            const_row=True
        )
        east_viewing_distance = viewing_distance(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            loop_forward=True,
            const_row=True
        )

        if is_visible_north or is_visible_south or is_visible_east or is_visible_west:
            num_visible_trees += 1

        # print(f"north_viewing_distance: {north_viewing_distance}")
        # print(f"south_viewing_distance: {south_viewing_distance}")
        # print(f"west_viewing_distance: {west_viewing_distance}")
        # print(f"east_viewing_distance: {east_viewing_distance}")
        scenic_score = north_viewing_distance * south_viewing_distance * west_viewing_distance * east_viewing_distance
        # print(f"\nscenic_score: {scenic_score}\n")
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print("PART 1")
print("======")
print(f"Number of visible trees: {num_visible_trees}")
print("======")
# Attempt 1: 3616 (too high)
# Attempt 2: 1794

print("PART 2")
print("======")
print(f"Highest scenic score: {max_scenic_score}")
print("======")
# Attempt 1: 2525952 (too high)
# Attempt 2: 199272
