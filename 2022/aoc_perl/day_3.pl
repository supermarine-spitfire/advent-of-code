#!/usr/bin/perl
use strict;
use warnings;

use FindBin;                                # Useful for finding directory where script is being invoked.
use lib "$FindBin::Bin/../aoc_perl/lib";    # Identifies library folder.

use set qw(make_set union intersection);
use util qw(file_to_array println print_hash);

sub make_priority_hash {
    my %args = (
        STARTING_ASCII_VALUE => 0,
        PRIORITY_START => 0,
        PRIORITY_END => 0,
        @_,
    );
    my $char_value = $args{STARTING_ASCII_VALUE};
    my $priority_start = $args{PRIORITY_START};
    my $priority_end = $args{PRIORITY_END};

    my %priorities = ();
    my $priority_value;
    for ($priority_value = $priority_start; $priority_value <= $priority_end; $priority_value++, $char_value++) {
        $priorities{chr($char_value)} = $priority_value;
    }

    return %priorities;
}

sub make_rucksack_set {
    my %args = (
        RUCKSACK_STR => "",
        @_
    );
    my $rucksack_str = $args{RUCKSACK_STR};

    my $elements = [];
    my $i;
    for ($i = 0; $i < length($rucksack_str); $i++) {
        push(@{$elements}, substr($rucksack_str, $i, 1));
    }
    return make_set(ELEMENTS => $elements);
}

println("Advent of Code 2022 Day 3");
println("-------------------------");

my @rucksacks = file_to_array(
    PATH_TO_FILE => "$FindBin::Bin/../input",
    FILE_NAME => "day-3-input.txt"
);

my %priorities = ();    # For easy access to priority values for characters.

# Lowercase letters mapped to priority values from 1 to 26.
%priorities = make_priority_hash(
    STARTING_ASCII_VALUE => 97, # ASCII/Unicode value for 'a'.
    PRIORITY_START => 1,
    PRIORITY_END => 26
);

# Uppercase letters mapped to priority values from 27 to 52.
%priorities = (
    %priorities,
    make_priority_hash(
        STARTING_ASCII_VALUE => 65, # ASCII/Unicode value for 'A'.
        PRIORITY_START => 27,
        PRIORITY_END => 52
    )
);

my $total_priorities = 0;
foreach my $rucksack (@rucksacks) {
    use integer;
    my $compartment1 = substr($rucksack, 0, length($rucksack) / 2);
    my $compartment2 = substr($rucksack, length($rucksack) / 2);
    # println("compartment1: $compartment1");
    # println("compartment2: $compartment2");

    my $elements = [];  # Used to collect items to put in sets.

    # Build sets representing compartments' contents.
    my $i;
    for ($i = 0; $i < length($compartment1); $i++) {
        push(@{$elements}, substr($compartment1, $i, 1));
    }
    my $compartment1_items = make_set(ELEMENTS => $elements);

    # print_hash(
    #     HASH_TO_PRINT => $compartment1_items,
    #     HASH_NAME => "compartment1_items"
    # );

    $elements = [];
    for ($i = 0; $i < length($compartment2); $i++) {
        push(@{$elements}, substr($compartment2, $i, 1));
    }
    my $compartment2_items = make_set(ELEMENTS => $elements);

    # print_hash(
    #     HASH_TO_PRINT => \%compartment2_items,
    #     HASH_NAME => "compartment2_items"
    # );

    # Get all items in common between both compartments.
    my $common_items = intersection(
        SET_1 => $compartment1_items,
        SET_2 => $compartment2_items
    );

    # Calculate total priority of common items.
    for my $k (keys %{$common_items}) {
        $total_priorities += $priorities{$k};
    }
}

println("PART 1");
println("======");
println("Total priorities: $total_priorities");
println("======");

$total_priorities = 0;
my $i;
for ($i = 0; $i <= scalar(@rucksacks) - 3; $i += 3) {
    println("i: $i");
    my $rucksack1_items = make_rucksack_set(RUCKSACK_STR => $rucksacks[$i]);
    my $rucksack2_items = make_rucksack_set(RUCKSACK_STR => $rucksacks[$i + 1]);
    my $rucksack3_items = make_rucksack_set(RUCKSACK_STR => $rucksacks[$i + 2]);

    my $common_items = intersection(
        SET_1 => $rucksack1_items,
        SET_2 => intersection(
            SET_1 => $rucksack2_items,
            SET_2 => $rucksack3_items
        )
    );

    # Calculate total priority of common items.
    for my $k (keys %{$common_items}) {
        $total_priorities += $priorities{$k};
    }
}

println("PART 2");
println("======");
println("Total priorities: $total_priorities");
