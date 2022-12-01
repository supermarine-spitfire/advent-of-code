import pathlib

def resolve_filepath(filename):
    return pathlib.PurePath(filename)

def file_to_list(filename):
    """Creates a list where each element corresponds to a line of a text file."""
    with open(resolve_filepath(filename)) as f:
        file_contents = f.read()
        return file_contents.split("\n")
