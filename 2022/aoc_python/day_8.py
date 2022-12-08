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

# print(f"tree_map:\n{tree_map}")
# First, calculate number of trees defining the border.
# General formula for the number of trees on the outside of an m x n grid is mn - (m - 2)(n - 2)
m = len(tree_map)       # Rows.
n = len(tree_map[0])    # Columns.
num_visible_trees = m * n - (m - 2) * (n - 2)
print(f"Number of border trees: {num_visible_trees}")
# Now iterate over the enclosed trees.
for row_index in range(1, m - 1):
    cur_row = tree_map[row_index]
    for col_index in range(1, n - 1):
        cur_tree = tree_map[row_index][col_index]
        # Look northward (column is constant, row decrements).
        is_visible_north = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            end_index=-1,
            const_row=False
        )

        # Look southward (column is constant, row increments).
        is_visible_south = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=col_index,
            start_index=row_index,
            end_index=m,
            const_row=False
        )

        # Look westward (row is constant, column decrements).
        is_visible_west = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            end_index=-1,
            const_row=True
        )

        # Look eastward (row is constant, column increments).
        is_visible_east = is_visible(
            tree_map=tree_map,
            tree=cur_tree,
            const_index=row_index,
            start_index=col_index,
            end_index=n,
            const_row=True
        )

        if is_visible_north or is_visible_south or is_visible_east or is_visible_west:
            num_visible_trees += 1


print("PART 1")
print("======")
print(f"Number of visible trees: {num_visible_trees}")
print("======")
# Attempt 1: 3616 (too high)
# Attempt 2: 1794