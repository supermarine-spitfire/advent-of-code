import functools
from enum import Enum

from lib import io

class Directory:
    def __init__(self, current_directory=None):
        self.current_directory = current_directory
        self.directories = []
        self.files = {}  # Maps file names to file sizes.
        self.children = []
        self.directory_size = 0
        # self.visited = False

    def add_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def add_file(self, file_name, file_size):
        self.files[file_name] = file_size
        # self.directory_size += int(file_size)

    # TODO: Alternate approach to consider for calculating directory and file sizes:
    # Store two sizes in each directory: total size of all contained files and total size of all contained directories.
    # Each time a file gets added to a directory, update that directory's total contained file size.
    # Then "bubble up" the newly added file's size to the directory's parent's total contained directory size.
    # Repeat until the root directory is reached.
    def update_total_size(self):
        # if self.visited:
            # return
        children_size = 0
        for child in self.children:
            children_size += child.total_size

        self.directory_size += children_size
        # self.visited = True
        # if self.children:
        #     for child in self.children:
        #         children_size += child.update_total_size()
        #     return children_size
        # else:
        #     return self.total_size

    def get_size_of_contents(self):
        return functools.reduce(lambda v, w: int(v) + int(w), self.files.values(), 0)

    def calculate_sizes(self):
        """Populates the directory_size fields of each Directory."""
        print(f"\nIn {self.current_directory}")
        total_size = self.get_size_of_contents()
        print(f"{self.current_directory}'s files' size: {total_size}")

        if not self.children:
            # Base case.
            # print("Base case.")
            print(f"total_size for items within {self.current_directory}: {total_size}")
            self.directory_size = total_size
            return total_size
        else:
            # Recursive case.
            print("Recursive case.")
            for child in self.children:
                total_size += child.calculate_sizes()
            print(f"\ntotal_size for items within {self.current_directory} (including items in subdirectories): {total_size}")
            self.directory_size = total_size
            return total_size

    def sum_filtered_sizes(self, upper_limit):
        """Returns the sum of the directory sizes that are less than or equal to upper_limit."""
        print(f"\nIn {self.current_directory}")
        total_size = self.directory_size if self.directory_size <= upper_limit else 0
        print(f"{self.current_directory}'s total_size (0 if greater than {upper_limit}): {total_size}")

        if not self.children:
            # Base case.
            print("Base case.")
            print(f"total_size for items within {self.current_directory}: {total_size}")
            return total_size
        else:
            # Recursive case.
            print("Recursive case.")
            for child in self.children:
                total_size += child.sum_filtered_sizes(upper_limit)
            print(f"\ntotal_size for items within {self.current_directory}: {total_size}")
            return total_size

    def __str__(self):
        return f"""current_directory: {self.current_directory if self.current_directory else ""}
directories: {self.directories if self.directories else "None"}
files: {self.files if self.files else "None"}
parent: {self.parent.current_directory if self.parent else "None"}
children: {[(c.current_directory, c.get_size_of_contents()) for c in self.children if c and self.children]}
size of contents: {self.get_size_of_contents()}
        """

    def __eq__(self, other):
        """Overrides default implementation."""
        if isinstance(other, Directory):
            return self.current_directory == other.current_directory \
                   and self.files == other.files \
                   and self.directory_size == other.directory_size

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
    # print(f"line: {line}")
    # Get each instruction on its own.
    instruction1 = line[0]
    instruction2 = line[1]
    instruction3 = line[2] if len(line) == 3 else ""

    # instruction1's value identifies if line is a terminal command, a directory, or a file.
    # instruction2's value is a file name, directory name, or a terminal command.
    if instruction1 == "$":
        # Found a terminal command.
        # print("Found terminal command.")
        if instruction2 == "cd":
            # cur_dir.update_total_size()
            # Time to change directories.
            # Three possible states:
            # 1. Move up one directory.
            # 2. Move up to root.
            # 3. Move down into a child directory.
            if instruction3 == "/":
                # Move to root.
                # print("Moving to root.")
                cur_dir = root
                # cur_dir.update_total_size()
            elif instruction3 == "..":
                # Move to parent directory.
                # print("Moving to parent directory.")
                cur_dir = cur_dir.parent
                # cur_dir.update_total_size()
            else:
                # Move to child directory.
                # print(f"Moving to child directory {instruction3}.")
                for child in cur_dir.children:
                    if child.current_directory == instruction3:
                        cur_dir = child
                        break
            # print(f"New cur_dir:\n{cur_dir}")
        elif instruction2 == "ls":
            # Listing items in current directory.
            continue
    elif instruction1 == "dir":
        # Found a directory; save its name.
        cur_dir.directories.append(instruction2)
        child_dir = Directory(current_directory=instruction2)
        if child_dir not in cur_dir.children:
            # print("Found new directory.")
            child_dir.add_parent(cur_dir)
            child_dir.current_directory = instruction2
            cur_dir.add_child(child_dir)
            # print(f"cur_dir:\n{cur_dir}")
    else:
        # Found a file; save its name and size.
        # print("Found new file.")
        cur_dir.add_file(file_name=instruction2, file_size=instruction1)
        # print(f"cur_dir:\n{cur_dir}")

print(f"root\n{root}")

# Traverse the directory structure.
print("Running calculate_sizes().")
total_size = root.calculate_sizes()
print("Running sum_filtered_sizes().")
total_filtered_size = root.sum_filtered_sizes(upper_limit=100000)

print("PART 1")
print("======")
print(f"Total size of root: {total_size}")
print(f"Total size of all directories of at most 100000: {total_filtered_size}")
print("======")
# Attempt 1: 1855262 (too high)
# Attempt 2: 1844187
