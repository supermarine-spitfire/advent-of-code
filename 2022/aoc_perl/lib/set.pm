package set 1.001;

use parent qw(Exporter);

use util qw(println);

our @EXPORT = qw(make_set union intersection);

sub make_set {
    # See https://stackoverflow.com/questions/3700037/how-can-i-represent-sets-in-perl
    # Hash keys that point to a common, undefined value enforces the uniqueness requirement of set elements.
    my %args = (
        ELEMENTS => [],
        @_
    );
    my $elements = $args{ELEMENTS};
    # println("elements: @{$elements}");

    my %set;
    @set{@{$elements}} = ();
    return \%set;
}

sub union {
    # Implements the union operation for two sets.
    my %args = (
        SET_1 => {},
        SET_2 => {},
        @_
    );
    my $set1_ref = $args{SET_1};
    my $set2_ref = $args{SET_2};

    my $all_items = ();
    for my $set1_key (keys %{$set1_ref}) {
        push(@{$all_items}, $set1_key);
    }
    for my $set2_key (keys %{$set2_ref}) {
        push(@{$all_items}, $set2_key);
    }

    return make_set(ELEMENTS => $all_items);
}

sub intersection {
    # Implements the intersection operation for two sets.
    my %args = (
        SET_1 => {},
        SET_2 => {},
        @_
    );
    my $set1_ref = $args{SET_1};
    my $set2_ref = $args{SET_2};

    my $common_items = ();
    for my $set1_key (keys %{$set1_ref}) {
        if (exists $set2_ref->{$set1_key}) {
            push(@{$common_items}, $set1_key);
        }
    }

    return make_set(ELEMENTS => $common_items);
}

1;