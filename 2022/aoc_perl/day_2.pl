#!/usr/bin/perl
use strict;
use warnings;

use FindBin;                                # Useful for finding directory where script is being invoked.
use lib "$FindBin::Bin/../aoc_perl/lib";    # Identifies library folder.

use util qw(file_to_array println);

print("Advent of Code 2022 Day 2\n");
print("-------------------------\n");

my @strategy_guide = file_to_array(
    PATH_TO_FILE => "$FindBin::Bin/../input",
    FILE_NAME => "day-2-input.txt"
);

# Read sums as outcome score plus shape score.
my %decision_table = ( # Start looking up by opponent, then by player.
    A => {  # Rock
        X => 3 + 1, # Rock: draw
        Y => 6 + 2, # Paper: win
        Z => 0 + 3  # Scissors: loss
    },
    B => {  # Paper
        X => 0 + 1, # Rock: loss
        Y => 3 + 2, # Paper: draw
        Z => 6 + 3  # Scissors: win
    },
    C => {  # Scissors
        X => 6 + 1, # Rock: win
        Y => 0 + 2, # Paper: loss
        Z => 3 + 3  # Scissors: draw
    }
);

# Calculate total score, assuming strategy guide is perfect.
my $total_score = 0;
for my $match (@strategy_guide) {
    my ($player_move, $opponent_move) = split(" ", $match);
    $total_score += $decision_table{$player_move}{$opponent_move};
}

println("PART 1");
println("======");
println("Total score (perfect strategy guide): $total_score");
println("======");

# Read sums as outcome score plus shape score.
%decision_table = ( # Start looking up by opponent's move, then by expected outcome
    A => {  # Rock
        X => 0 + 3, # Loss: play scissors.
        Y => 3 + 1, # Draw: play rock.
        Z => 6 + 2  # Win: play paper.
    },
    B => {  # Paper
        X => 0 + 1, # Loss: play rock.
        Y => 3 + 2, # Draw: play paper.
        Z => 6 + 3  # Win: play scissors.
    },
    C => {  # Scissors
        X => 0 + 2, # Loss: play paper.
        Y => 3 + 3, # Draw: play scissors.
        Z => 6 + 1  # Win: play rock.
    }
);

# Calculate total score, assuming strategy guide describes what each match's outcome is.
$total_score = 0;
for my $match (@strategy_guide) {
    my ($player_move, $opponent_move) = split(" ", $match);
    $total_score += $decision_table{$player_move}{$opponent_move};
}

println("PART 2");
println("======");
println("Total score (outcome strategy guide): $total_score");
println("======");
