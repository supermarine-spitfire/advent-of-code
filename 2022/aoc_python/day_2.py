from lib import io

print("Advent of Code 2022 Day 2")
print("-------------------------")
strategy_guide = io.file_to_list("input/day-2-input.txt")

# Read sums as outcome score plus shape score.
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

# Calculate total score, assuming strategy guide is perfect.
total_score = 0
for match in strategy_guide:
    player_move, opponent_move = match.split(" ")
    total_score += decision_matrix[player_move][opponent_move]

print("PART 1")
print("======")
print(f"Total score (perfect strategy guide): {total_score}")
print("======")

# Read sums as outcome score plus shape score.
decision_matrix = { # Start looking up by opponent's move, then by expected outcome
    "A": {  # Rock
        "X": 0 + 3, # Loss: play scissors.
        "Y": 3 + 1, # Draw: play rock.
        "Z": 6 + 2  # Win: play paper.
    },
    "B": {  # Paper
        "X": 0 + 1, # Loss: play rock.
        "Y": 3 + 2, # Draw: play paper.
        "Z": 6 + 3  # Win: play scissors.
    },
    "C": {  # Scissors
        "X": 0 + 2, # Loss: play paper.
        "Y": 3 + 3, # Draw: play scissors.
        "Z": 6 + 1  # Win: play rock.
    }
}

# Calculate total score, assuming strategy guide describes what each match's outcome is.
total_score = 0
for match in strategy_guide:
    player_move, opponent_move = match.split(" ")
    total_score += decision_matrix[player_move][opponent_move]


print("PART 2")
print("======")
print(f"Total score (outcome strategy guide): {total_score}")
print("======")
