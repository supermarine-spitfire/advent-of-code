from lib import io

print("Advent of Code 2022 Day 6")
print("-------------------------")
signal_input = io.file_to_string("input/day-6-input.txt")

def find_unique_substring_starting_index(str, substring_length):
    starting_index = substring_length
    while starting_index < len(str):
        if len(set(str[starting_index - substring_length : starting_index])) == substring_length:
            # Found start-of-substring marker (since sets do not hold duplicates).
            break
        else:
            starting_index += 1

    return starting_index

# Sweep a window of size 4 across signal_input, looking for a substring of 4 unique characters.
start_of_packet_index = find_unique_substring_starting_index(str=signal_input, substring_length=4)

print("PART 1")
print("======")
print(f"First marker index: {start_of_packet_index}")
print("======")
# Attempt 1: 1658.

