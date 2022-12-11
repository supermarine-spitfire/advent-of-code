import queue

from functools import reduce

from lib import io

class Monkey:
    def __init__(self, starting_items, operation, divisor, true_target, false_target):
        self.items = queue.Queue()
        for item in starting_items:
            self.items.put(item)

        self.operation = operation
        self.divisible_by = divisor
        self.true_target = true_target
        self.false_target = false_target

        self.current_worry_level = 0
        self.num_inspections = 0

    def __operation__(self, old):
        return eval(self.operation, {"old": old})

    def has_items(self):
        return not self.items.empty()

    def inspect_item(self):
        # print("In inspect_item().")
        # Get first item.
        self.current_worry_level = self.items.get()
        self.current_worry_level = self.__operation__(self.current_worry_level)
        self.num_inspections += 1

    def throw_item(self, relief_function):
        # print("In throw_item().")
        # Worry level first decreases, if applicable.
        if relief_function:
            self.current_worry_level = relief_function(self.current_worry_level)

        # Once decrease happens, monkey throws it to another monkey.
        if self.current_worry_level % self.divisible_by == 0:
            return self.current_worry_level, self.true_target
        else:
            return self.current_worry_level, self.false_target

    def catch_item(self, item):
        # print("In catch_item().")
        self.items.put(item)

    def __str__(self) -> str:
        return f"""Carried items: {self.items}
Worry level of item being inspected: {self.current_worry_level}
Target if worry level is divisible by {self.divisible_by}: {self.true_target}.
Target if worry level is not divisible by {self.divisible_by}: {self.false_target}.
Number of inspections: {self.num_inspections}
"""

    __repr__ = __str__


def get_monkeys(monkey_configuration):
    monkeys = {}
    i = 0
    while i < len(monkey_configuration) - 6:
        # print(f"i: {i}")
        monkey_index = int(monkey_configuration[i].split(" ")[1].strip(":"))
        monkey_starting_items = monkey_configuration[i + 1]
        monkey_operation = monkey_configuration[i + 2]
        monkey_test = monkey_configuration[i + 3 : i + 6]

        # Make starting list.
        monkey_starting_items = [int(msi)
            for msi in monkey_starting_items.split(":")[1].strip().split(",")
        ]
        # print(f"monkey_starting_items: {monkey_starting_items}")

        # Make operation.
        # Consider using eval() with values for "old", "new" passed in via a dictionary.
        monkey_operation = monkey_operation.split("=")[1]

        # Make test.
        divisor = int(monkey_test[0].split(" ")[-1])
        true_destination = int(monkey_test[1].split(" ")[-1])
        false_destination = int(monkey_test[2].split(" ")[-1])

        monkeys[monkey_index] = Monkey(
            starting_items=monkey_starting_items,
            operation=monkey_operation,
            divisor=divisor,
            true_target=true_destination,
            false_target=false_destination
        )

        i += 7  # Skip over the newline separating monkeys.

    return monkeys


def simulate_rounds(monkeys, num_rounds, relief_function):
    for i in range(num_rounds):
        # print(f"Round {i + 1}.")
        for j in range(len(monkeys)):
            # print(f"Current monkey: {j}")
            # Each round has each monkey take a turn inspecting one item.
            cur_monkey = monkeys[j]
            # print(f"cur_monkey: {cur_monkey}")
            while cur_monkey.has_items():
                cur_monkey.inspect_item()
                item, target_monkey = cur_monkey.throw_item(relief_function=relief_function)
                monkeys[target_monkey].catch_item(item)


def get_monkey_business(monkeys):
    # Get number of times each monkey inspected items ("inspection count").
    monkey_inspection_counts = {
        monkey_index : monkey.num_inspections
        for monkey_index, monkey in monkeys.items()
    }
    print(f"monkey_inspections_counts: {monkey_inspection_counts}")

    # Calculate monkey business (defined as product of each monkey's inspection count).
    monkey_scores = sorted(monkey_inspection_counts.values())[-2:] # Only count top two scores.
    monkey_business = reduce(lambda x, y: x * y, monkey_scores)

    return monkey_business


def get_large_relief_function(monkeys):
    # This relief function is defined as f(x) = x mod N,
    # where N is the product of each monkey's divisor.
    divisors = [
        monkey.divisible_by for monkey in monkeys.values()
    ]
    composite_divisor = reduce(lambda x, y: x * y, divisors)
    return lambda n: n % composite_divisor


print("Advent of Code 2022 Day 11")
print("-------------------------")
monkey_configuration = io.file_to_list("input/day-11-input.txt")
# monkey_configuration = io.file_to_list("input/day-11-test-data.txt")

# Get the monkey information.
monkeys = get_monkeys(monkey_configuration)
# print(f"monkeys: {monkeys}")

# Simulate 20 rounds of the monkeys throwing items.
simulate_rounds(monkeys=monkeys, num_rounds=20, relief_function=lambda x: x // 3)
monkey_business = get_monkey_business(monkeys=monkeys)

print("PART 1")
print("======")
print(f"Level of monkey business: {monkey_business}")
print("======")
# Attempt 1: 316888

# Simulate 10000 rounds of the monkeys throwing items.
monkeys = get_monkeys(monkey_configuration)
# print(f"monkeys: {monkeys}")
large_relief_function = get_large_relief_function(monkeys)
simulate_rounds(monkeys=monkeys, num_rounds=10000, relief_function=large_relief_function)
monkey_business = get_monkey_business(monkeys=monkeys)

print("PART 2")
print("======")
print(f"Level of monkey business: {monkey_business}")
# Attempt 1: 38214971410 (too high)
# Attempt 2: 35270398814
