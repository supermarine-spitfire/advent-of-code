from lib import io

print("Advent of Code 2022 Day 2")
print("-------------------------")
strategy_guide = io.file_to_list("input/day-2-input.txt")

# Calculate total score, assuming strategy guide is perfect.
decision_matrix = { # Start looking up by opponent, then by player.
    "A": {  # Rock
        "X": 3 + 1, # Rock: draw
        "Y": 6 + 2, # Paper: win
        "Z": 0 + 3  # Scissors: loss
    },
    "B": {  # Paper
        "X": 0 + 1, # Rock: loss
        "Y": 3 + 2, # Paper: draw
        "Z": 6 + 3  # Scissors: win
    },
    "C": {  # Scissors
        "X": 6 + 1, # Rock: win
        "Y": 0 + 2, # Paper: loss
        "Z": 3 + 3  # Scissors: draw
    }
}

if_statement_total_score = 0
total_score = 0
for match in strategy_guide:
    player_move, opponent_move = match.split(" ")
    total_score += decision_matrix[player_move][opponent_move]

print("PART 1")
print("======")
print(f"Total score: {total_score}")
print("======")

