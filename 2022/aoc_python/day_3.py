from lib import io

print("Advent of Code 2022 Day 3")
print("-------------------------")
rucksacks = io.file_to_list("input/day-3-input.txt")
# print(f"rucksacks: {rucksacks}")

priorities = {chr(k): v for (k, v) in zip(range(97, 123), range(1, 27))}        # Lowercase letters mapped to priority values from 1 to 26.
priorities.update({chr(k): v for (k, v) in zip(range(65, 91), range(27, 53))})  # Uppercase letters mapped to priority values from 27 to 52.

total_priorities = 0
for rucksack in rucksacks:
    # Get all items in common between both compartments.
    compartment_1 = rucksack[:len(rucksack) // 2]
    compartment_2 = rucksack[len(rucksack) // 2:]
    # print(f"compartment_1: {compartment_1}")
    # print(f"compartment_2: {compartment_2}")
    common_items = set(item for item in compartment_1 if item in compartment_2)
    # print(f"common_items: {common_items}")

    # Calculate total priority of common items.
    total_priorities += sum(priorities[item] for item in common_items)

print("PART 1")
print("======")
print(f"Total priorities: {total_priorities}")
print("======")
# Attempt 1: 10716 (too high)
# Attempt 2: 7917 (correct)

