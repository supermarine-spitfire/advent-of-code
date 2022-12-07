#!/usr/bin/perl
use strict;
use warnings;

use FindBin;                                # Useful for finding directory where script is being invoked.
use lib "$FindBin::Bin/../aoc_perl/lib";    # Identifies library folder.

use util qw(file_to_array println print_hash);

println("Advent of Code 2022 Day 4");
println("-------------------------");

my @section_assignment_pairs = file_to_array(
    PATH_TO_FILE => "$FindBin::Bin/../input",
    FILE_NAME => "day-4-input.txt"
);

my $num_fully_contained_pairs = 0;
my $num_overlapping_pairs = 0;
for my $section_pair (@section_assignment_pairs) {
    # Get each section assignment.
    my ($section1, $section2) = split(",", $section_pair);

    # Get lower and upper limits (ll and ul, respectively) of each section assignment.
    my ($section_1_ll, $section_1_ul) = split("-", $section1);
    my ($section_2_ll, $section_2_ul) = split("-", $section2);

    # Prevent the if conditions from using lexical ordering instead of numerical ordering.
    $section_1_ll = int($section_1_ll);
    $section_2_ll = int($section_2_ll);
    $section_1_ul = int($section_1_ul);
    $section_2_ul = int($section_2_ul);

    # Find section assignment ranges that completely overlap each other.
    # Case 1: Section 1 fully encloses Section 2.
    # Case 2: Section 2 fully encloses Section 1.
    # Case 3: Section 1 and Section 2 share same start but Section 1 ends before Section 2.
    # Case 4: Section 1 and Section 2 share same start but Section 2 ends before Section 1.
    # Case 5: Section 1 and Section 2 share same end but Section 1 starts before Section 2.
    # Case 6: Section 1 and Section 2 share same end but Section 2 starts before Section 1.
    # Case 7: Section 1 and Section 2 are identical ranges.
    if (
            ($section_1_ll < $section_2_ll && $section_1_ul > $section_2_ul)
         || ($section_2_ll < $section_1_ll && $section_2_ul > $section_1_ul)
         || ($section_2_ll == $section_1_ll && $section_1_ul < $section_2_ul)
         || ($section_2_ll == $section_1_ll && $section_2_ul < $section_1_ul)
         || ($section_2_ll > $section_1_ll && $section_2_ul == $section_1_ul)
         || ($section_2_ll < $section_1_ll && $section_2_ul == $section_1_ul)
         || ($section_2_ll == $section_1_ll && $section_2_ul == $section_1_ul)
    ) {
        $num_fully_contained_pairs += 1;
    }

    # Find section assignment ranges that overlap in some way.
    # Case 1: Section 1 and Section 2 are identical ranges.
    # Case 2: Section 1 fully encloses Section 2.
    # Case 3: Section 2 fully encloses Section 1.
    # Case 4: Section 1 and Section 2 share same start.
    # Case 5: Section 1 and Section 2 share same end.
    # Case 6: Section 1 starts inside Section 2.
    # Case 7: Section 2 starts inside Section 1.
    # Case 8: Section 1 ends inside Section 2.
    # Case 9: Section 2 ends inside Section 1.
    if (
            ($section_2_ll == $section_1_ll && $section_2_ul == $section_1_ul)
         || ($section_1_ll < $section_2_ll && $section_1_ul > $section_2_ul)
         || ($section_2_ll < $section_1_ll && $section_2_ul > $section_1_ul)
         || ($section_1_ll == $section_2_ll)
         || ($section_1_ul == $section_2_ul)
         || ($section_1_ll >= $section_2_ll && $section_1_ll <= $section_2_ul)
         || ($section_2_ll >= $section_1_ll && $section_2_ll <= $section_1_ul)
         || ($section_1_ul >= $section_2_ll && $section_1_ul <= $section_2_ul)
         || ($section_2_ul >= $section_1_ll && $section_2_ul <= $section_1_ul)
    ) {
        $num_overlapping_pairs += 1;
    }
}

println("PART 1");
println("======");
println("Number of fully contained range assignment pairs: $num_fully_contained_pairs");
println("======");

println("PART 2");
println("======");
println("Number of overlapping range assignment pairs: $num_overlapping_pairs");
