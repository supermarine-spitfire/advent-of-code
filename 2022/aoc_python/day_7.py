import functools
from enum import Enum

from lib import io

class InstructionType(Enum):
    TERMINAL_OUTPUT = 1
    DIRECTORY = 2
    FILE = 3

class Directory:
    def __init__(self, current_directory=None):
        self.current_directory = current_directory
        self.directories = []
        self.files = {}  # Maps file names to file sizes.
        self.children = []
        self.total_size = 0
        self.visited = False

    def add_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def add_file(self, file_name, file_size):
        self.files[file_name] = file_size
        self.total_size += int(file_size)

    def update_total_size(self):
        if self.visited:
            return
        children_size = 0
        for child in self.children:
            children_size += child.total_size

        self.total_size += children_size
        self.visited = True
        # if self.children:
        #     for child in self.children:
        #         children_size += child.update_total_size()
        #     return children_size
        # else:
        #     return self.total_size

    def get_total_size(self):
        return functools.reduce(lambda v, w: int(v) + int(w), self.files.values(), 0)

    def traverse_for_sizes(self, upper_limit):
        total_size = self.total_size if self.total_size <= upper_limit else 0
        # total_size = dir.get_total_size() if dir.total_size <= upper_limit else 0

        if not self.children:
            # Base case.
            return total_size
        else:
            # Recursive case.
            for child in self.children:
                total_size += child.traverse_for_sizes(upper_limit)
            return total_size

    def __str__(self):
        return f"""current_directory: {self.current_directory if self.current_directory else ""}
directories: {self.directories if self.directories else "None"}
files: {self.files if self.files else "None"}
parent: {self.parent.current_directory if self.parent else "None"}
children: {[(c.current_directory, c.total_size) for c in self.children if c and self.children]}
total_size: {self.total_size}
visited: {self.visited}
        """

    def __eq__(self, other):
        """Overrides default implementation."""
        if isinstance(other, Directory):
            return self.current_directory == other.current_directory \
                   and self.files == other.files \
                   and self.total_size == other.total_size

        return False


print("Advent of Code 2022 Day 7")
print("-------------------------")
# terminal_output = io.file_to_list("input/day-7-test-data.txt")
# terminal_output = io.file_to_list("input/day-7-test-data-2.txt")
terminal_output = io.file_to_list("input/day-7-input.txt")
terminal_output = [s.split(" ") for s in terminal_output]

# Identify all files and directories, along with their sizes.
# Define the topmost directory.
root = Directory(current_directory="/")
root.add_parent(None)
cur_dir = root
for line in terminal_output:
    print(f"line: {line}")
    # Get each instruction on its own.
    instruction1 = line[0]
    instruction2 = line[1]
    instruction3 = line[2] if len(line) == 3 else ""

    # instruction1's value identifies if line is a terminal command, a directory, or a file.
    if instruction1 == "$":
        # Terminal command.
        cur_instruct = InstructionType.TERMINAL_OUTPUT
    elif instruction1 == "dir":
        # Directory.
        cur_instruct = InstructionType.DIRECTORY
    else:
        # File.
        cur_instruct = InstructionType.FILE

    # instruction2 is a file name, directory name, or a terminal command.
    if cur_instruct == InstructionType.FILE:
        # Found a file; save its name and size.
        print("Found new file.")
        cur_dir.add_file(file_name=instruction2, file_size=instruction1)
        print(f"cur_dir:\n{cur_dir}")
    elif cur_instruct == InstructionType.DIRECTORY:
        # Found a directory; save its name.
        cur_dir.directories.append(instruction2)
        child_dir = Directory(current_directory=instruction2)
        if child_dir not in cur_dir.children:
            print("Found new directory.")
            child_dir.add_parent(cur_dir)
            child_dir.current_directory = instruction2
            cur_dir.add_child(child_dir)
            print(f"cur_dir:\n{cur_dir}")
    else:
        # Terminal command.
        print("Found terminal command.")
        if instruction2 == "cd":
            # cur_dir.update_total_size()
            # Time to change directories.
            # Three possible states:
            # 1. Move up one directory.
            # 2. Move up to root.
            # 3. Move down into a child directory.
            if instruction3 == "/":
                # Move to root.
                print("Moving to root.")
                cur_dir = root
                cur_dir.update_total_size()
            elif instruction3 == "..":
                # Move to parent directory.
                print("Moving to parent directory.")
                cur_dir = cur_dir.parent
                cur_dir.update_total_size()
            else:
                # Move to child directory.
                print(f"Moving to child directory {instruction3}.")
                for child in cur_dir.children:
                    if child.current_directory == instruction3:
                        cur_dir = child
                        break
            print(f"New cur_dir:\n{cur_dir}")
        elif instruction2 == "ls":
            # Listing items in current directory.
            continue

print(f"root\n{root}")

# Traverse the directory structure.
total_size = root.traverse_for_sizes(upper_limit=100000)

print("PART 1")
print("======")
print(f"Total size of all directories of at most 100000: {total_size}")
print("======")
# Attempt 1: 1855262 (too high)