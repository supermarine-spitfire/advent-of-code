#!/usr/bin/perl
use strict;
use warnings;

use Path::Tiny;
use autodie;

print("Advent of Code 2022 Day 1\n");
print("-------------------------\n");

# Load calorie counts.
my $dir = path("input");
my $calorie_file = $dir->child("day-1-input.txt");
my $file_handle = $calorie_file->openr_utf8();

my @calorie_counts = ();
while ( my $line = $file_handle->getline() ) {
    $line =~ s/^\s+|\s+$//g;    # Trims whitespace from before and after line.
    unshift(@calorie_counts, $line);    # Enqueue operation.
}
close($file_handle);
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
print("PART 2");
print("======");
my $top_three_calorie_sum = $total_calories[0] + $total_calories[1] + $total_calories[2];
print("Top three calorie sum: $top_three_calorie_sum\n");
