from lib import io

print("Advent of Code 2022 Day 4")
print("-------------------------")
section_assignment_pairs = io.file_to_list("input/day-4-input.txt")

num_fully_contained_pairs = 0
num_overlapping_pairs = 0
for section_pair in section_assignment_pairs:
    # Get each section assignment.
    section_1, section_2 = section_pair.split(",")

    # Get lower and upper limits (ll and ul, respectively) of each section assignment.
    section_1_ll, section_1_ul = section_1.split("-")
    section_2_ll, section_2_ul = section_2.split("-")

    # Prevent the if conditions from using lexical ordering instead of numerical ordering.
    section_1_ll = int(section_1_ll)
    section_2_ll = int(section_2_ll)
    section_1_ul = int(section_1_ul)
    section_2_ul = int(section_2_ul)

    # Find section assignment ranges that completely overlap each other.
    # Case 1: Section 1 fully encloses Section 2.
    # Case 2: Section 2 fully encloses Section 1.
    # Case 3: Section 1 and Section 2 share same start but Section 1 ends before Section 2.
    # Case 4: Section 1 and Section 2 share same start but Section 2 ends before Section 1.
    # Case 5: Section 1 and Section 2 share same end but Section 1 starts before Section 2.
    # Case 6: Section 1 and Section 2 share same end but Section 2 starts before Section 1.
    # Case 7: Section 1 and Section 2 are identical ranges.
    if    (section_1_ll < section_2_ll and section_1_ul > section_2_ul)  \
       or (section_2_ll < section_1_ll and section_2_ul > section_1_ul)  \
       or (section_2_ll == section_1_ll and section_1_ul < section_2_ul) \
       or (section_2_ll == section_1_ll and section_2_ul < section_1_ul) \
       or (section_2_ll > section_1_ll and section_2_ul == section_1_ul) \
       or (section_2_ll < section_1_ll and section_2_ul == section_1_ul) \
       or (section_2_ll == section_1_ll and section_2_ul == section_1_ul):
        num_fully_contained_pairs += 1

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
    if    (section_2_ll == section_1_ll and section_2_ul == section_1_ul)   \
       or (section_1_ll < section_2_ll and section_1_ul > section_2_ul)     \
       or (section_2_ll < section_1_ll and section_2_ul > section_1_ul)     \
       or (section_1_ll == section_2_ll)                                    \
       or (section_1_ul == section_2_ul)                                    \
       or (section_1_ll >= section_2_ll and section_1_ll <= section_2_ul)   \
       or (section_2_ll >= section_1_ll and section_2_ll <= section_1_ul)   \
       or (section_1_ul >= section_2_ll and section_1_ul <= section_2_ul)   \
       or (section_2_ul >= section_1_ll and section_2_ul <= section_1_ul):
        num_overlapping_pairs += 1

print("PART 1")
print("======")
print(f"Number of fully contained range assignment pairs: {num_fully_contained_pairs}")
print("======")
# Attempt 1: 535.
# Attempt 2: 241.
# Attempt 3: 512.
# Attempt 4: 466.

print("PART 2")
print("======")
print(f"Number of overlapping range assignment pairs: {num_overlapping_pairs}")
# Attempt 1: 751 (too low).
# Attempt 2: 865.
