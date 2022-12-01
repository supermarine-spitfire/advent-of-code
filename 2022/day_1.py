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

# Get highest calorie count.
total_calories.sort()
print("PART 1")
print("======")
print(f"Highest calorie count: {total_calories[0]}")
print("======")

# Get sum of top three calorie counts.
print("PART 2")
print("======")
top_three_calorie_sum = total_calories.pop() + total_calories.pop() + total_calories.pop()
print(f"Top three calorie sum: {top_three_calorie_sum}")
