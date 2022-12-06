package util 1.001;

use Path::Tiny;
use FindBin;
use autodie;

use parent qw(Exporter);

our @EXPORT = qw(file_to_array println print_hash);

sub file_to_array {
    my %args = (
        PATH_TO_FILE => "",
        FILE_NAME => "",
        @_,
    );

    # print("PATH_TO_FILE: $args{PATH_TO_FILE}\n");
    # print("FILE_NAME: $args{FILE_NAME}\n");
    my $file = path($args{PATH_TO_FILE})->child($args{FILE_NAME});

    my @file_array = $file->lines({chomp => 1});  # Strips off newlines from each line.
    # print("file_array:\n");
    # for my $line (@file_array) {
        # print("line: $line\n");
    # }
    return @file_array;
}

sub println {
    print(@_, "\n");
}

sub print_hash {
    my %args = (
        HASH_TO_PRINT => {},
        HASH_NAME => "",
        @_
    );
    my $hash_ref = $args{HASH_TO_PRINT};
    my $hash_name = $args{HASH_NAME};

    println("Contents of $hash_name:");
    for my $key (keys %{$hash_ref}) {
        println("$key => ${$hash_ref}{$key}");
    }
}

1;
