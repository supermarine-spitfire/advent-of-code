#!/usr/bin/perl
use strict;
use warnings;

use FindBin;                                # Useful for finding directory where script is being invoked.
use lib "$FindBin::Bin/../aoc_perl/lib";    # Identifies library folder.

use util qw(file_to_array println print_hash);

println("Advent of Code 2022 Day 5");
println("-------------------------");

my @file_contents = file_to_array(
    PATH_TO_FILE => "$FindBin::Bin/../input",
    FILE_NAME => "day-5-input.txt"
);

# Figure out where initial conditions end and instructions begin.
my $i = 0;
while ($file_contents[$i] ne "") {
    $i += 1;
}

# Split input into initial conditions and instructions.
my @initial_conditions = $file_contents[0..$i];  # Strips out the empty line.
my $instructions = $file_contents[$i + 1..$#file_contents];    # See above.

# Construct stacks and their initial contents.
my $max_length = length($initial_conditions[0]);         # Guaranteed all lines in section are same length.
my $stack_labels = split(" ", $initial_conditions[-1]);   # At bottom of section.
# print(f"stack_labels: {stack_labels}")
# my $stacks_for_single_move_crane = { k: [] for k in stack_labels}