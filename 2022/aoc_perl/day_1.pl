#!/usr/bin/perl
use strict;
use warnings;

use FindBin;                                # Useful for finding directory where script is being invoked.
use lib "$FindBin::Bin/../aoc_perl/lib";    # Identifies library folder.

use util qw(file_to_array println);

print("Advent of Code 2022 Day 1\n");
print("-------------------------\n");

# Load calorie counts.
my @calorie_counts = file_to_array(
    PATH_TO_FILE => "$FindBin::Bin/../input",
    FILE_NAME => "day-1-input.txt"
);
# print("calorie_counts: @calorie_counts\n");

# Get total calories carried by each elf.
my @total_calories = ();
my $calorie_sum = 0;
for my $calorie_count (@calorie_counts) {
    # print("calorie_count: $calorie_count\n");
    if ($calorie_count) {
        # print("Truthy.\n");
        $calorie_sum += int($calorie_count);
        # print("calorie_sum: $calorie_sum\n");
    } else {
        # print("Falsey.\n");
        unshift(@total_calories, $calorie_sum);
        # print("total_calories: @total_calories\n");
        $calorie_sum = 0;
    }
}

# Get highest calorie count.
@total_calories = sort { $b <=> $a } @total_calories;   # Sort numerically in descending order.
print("PART 1\n");
print("======\n");
print("Highest calorie count: $total_calories[0]\n");
print("======\n");

# Get sum of top three calorie counts.
print("PART 2\n");
print("======\n");
my $top_three_calorie_sum = $total_calories[0] + $total_calories[1] + $total_calories[2];
print("Top three calorie sum: $top_three_calorie_sum\n");
