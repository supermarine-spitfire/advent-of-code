from lib import io

print("Advent of Code 2022 Day 1")
print("-------------------------")
# Load calorie counts.
calorie_log_file = "input/day-1-input.txt"
calorie_counts = io.file_to_list(calorie_log_file)

# Get total calories carried by each elf.
total_calories = []
calorie_sum = 0
for calorie_count in calorie_counts:
    if calorie_count:
        calorie_sum += int(calorie_count)
    else:
        total_calories.append(calorie_sum)
        calorie_sum = 0

# Get maximum calorie count.
total_calories.sort()
print (f"len(calorie_counts): {len(calorie_counts)}")
print (f"len(total_calories): {len(total_calories)}")
print(f"Highest calorie count: {total_calories[-1]}")
