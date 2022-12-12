import pathlib

def resolve_filepath(filename):
    return pathlib.PurePath(filename)

def file_to_list(filename):
    """Creates a list where each element corresponds to a line of a text file."""
    with open(resolve_filepath(filename)) as f:
        file_contents = f.read()
        return file_contents.split("\n")

def file_to_string(filename):
    """Returns the contents of a text file as one string."""
    with open(resolve_filepath(filename)) as f:
        return f.read()

def file_dimensions(filename):
    """Returns the number of columns and rows in a text file.

        Assumes all rows are the same length and the first line is non-empty.
    """
    file_contents = file_to_list(filename)
    return len(file_contents), len(file_contents[0])
