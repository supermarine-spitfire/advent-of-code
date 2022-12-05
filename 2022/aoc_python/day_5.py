import copy
import re

from lib import io

print("Advent of Code 2022 Day 5")
print("-------------------------")
file_contents = io.file_to_list("input/day-5-input.txt")

# Figure out where initial conditions end and instructions begin.
i = 0
while file_contents[i]:
    i += 1

# Split input into initial conditions and instructions.
initial_conditions = file_contents[:i]  # Strips out the empty line.
instructions = file_contents[i + 1:]    # See above.

# Construct stacks and their initial contents.
max_length = len(initial_conditions[0])         # Guaranteed all lines in section are same length.
stack_labels = initial_conditions[-1].split()   # At bottom of section.
# print(f"stack_labels: {stack_labels}")
stacks_for_single_move_crane = { k: [] for k in stack_labels}

stack_contents = initial_conditions[:-1]
stack_pattern = re.compile(r"\[\w\]")
for level in reversed(stack_contents):
    # Sweep a window of size three across level; this captures the crate if present.
    cur_level_index = 0
    cur_stack_index = 0
    while cur_level_index <= len(level) - 3:
        cur_stack_contents = level[cur_level_index:cur_level_index + 3]
        # print(f"cur_stack_contents: {cur_stack_contents}")
        if stack_pattern.match(cur_stack_contents):
            # Crate found; push it onto the current stack.
            # print("Crate found.\n")
            stacks_for_single_move_crane[stack_labels[cur_stack_index]].append(level[cur_level_index + 1])
        # else:
            # No crate found; advance to next stack.
            # print("Crate not found.\n")

        cur_stack_index += 1
        cur_level_index += 4    # Skip over the space separating each stack.

stacks_for_multi_move_crane = copy.deepcopy(stacks_for_single_move_crane)
# print(f"stacks_for_single_move_crane (initial): {stacks_for_single_move_crane}")

# Now parse the instructions.
for instruction in instructions:
    # print(f"instruction: {instruction}")
    instruction_list = instruction.split()  # All instructions will have 6 elements when split.
    num_crates = int(instruction_list[1])
    source_stack = instruction_list[3]
    target_stack = instruction_list[5]

    # Move crates according to instructions.
    for i in range(num_crates):
        crate = stacks_for_single_move_crane[source_stack].pop()
        stacks_for_single_move_crane[target_stack].append(crate)

# print(f"stacks_for_single_move_crane (final): {stacks_for_single_move_crane}")

# Get list of crates on top.
top_crates = ""
for stack in stacks_for_single_move_crane.values():
    top_crates += stack.pop()

print("PART 1")
print("======")
print(f"Crates on top: {top_crates}")
print("======")
# Attempt 1: TWSGQHNHL (correct)

# print(f"stacks_for_multi_move_crane (initial): {stacks_for_multi_move_crane}")
# Parse the instructions assuming crane preserves order of removed crates.
for instruction in instructions:
    # print(f"instruction: {instruction}")
    instruction_list = instruction.split()  # All instructions will have 6 elements when split.
    num_crates = int(instruction_list[1])
    source_stack = instruction_list[3]
    target_stack = instruction_list[5]

    # Move crates according to instructions.
    # Moving multiple crates whilst preserving order can be modelled by pushing the crates onto
    # a "buffer stack" and then emptying the buffer stack onto the target stack.
    buffer_stack = []
    for i in range(num_crates):
        buffer_stack.append(stacks_for_multi_move_crane[source_stack].pop())

    while buffer_stack:
        stacks_for_multi_move_crane[target_stack].append(buffer_stack.pop())

# print(f"stacks_for_multi_move_crane (final): {stacks_for_multi_move_crane}")

# Get list of crates on top.
top_crates = ""
for stack in stacks_for_multi_move_crane.values():
    top_crates += stack.pop()

print("PART 2")
print("======")
print(f"Crates on top: {top_crates}")
