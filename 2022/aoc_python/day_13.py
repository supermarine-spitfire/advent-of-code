from lib import io


def check_packets(left_packet, right_packet):
    print("In check_packets().")
    print(f"left_packet: {left_packet}")
    print(f"right_packet: {right_packet}")
    # General algorithm:
    # Split left and right packets (each a list) into two pieces each: call them head and tail.
    # The head is the first element of each packet list; the tail, the remaining elements of the packet lists.
    # Check the heads of left and right according to the cases outlined below.
    # Recursively check the tails of left and right according to the cases outlined above.
    # AND the result of the head check with that of the tail check and return the result.
    #
    # Cases to consider for proper order:
    # 1. If both current elements are integers, the left one must be less than the right one for the packet pair to be in order.
    # 2. If both current elements are lists, recursively check each current element's values according to the cases defined herein.
    #    If the left element list runs out before the right element list, the packet pair is in order.
    # 3. If exactly one of the elements is an integer, convert that integer to a list and apply Case 2.

    # These conditions check if Case 2's base sub-case is triggered.
    if len(left_packet) == 0:
        print("Case 2 triggered; left ran out first or both ran out at same time.")
        return True     # A tentative true value; following recursive calls may cancel it out.
    elif len(right_packet) == 0:
        print("Case 2 triggered; right ran out first.")
        return False    # Right ended before left: hence out of order.

    # Split packets into their heads and tails.
    left_head = left_packet[0]
    right_head = right_packet[0]
    left_tail = left_packet[1:]
    right_tail = right_packet[1:]
    print(f"left_head: {left_head}")
    print(f"right_head: {right_head}")
    print(f"left_tail: {left_tail}")
    print(f"right_tail: {right_tail}")
    # if len(left_packet) > 1:
    #     left_tail = left_packet[1:]
    # if len(right_packet) > 1:
    #     right_tail = right_packet[1:]

    # Check Case 1.
    if isinstance(left_head, int) and isinstance(right_head, int):
        print("Case 1 triggered: left_head and right_head are integers.")
        if left_head < right_head:
            print(f"{left_head} < {right_head}")
            return True
        elif left_head == right_head:
            print(f"{left_head} = {right_head}: recursively check tails of packets.")
            return check_packets(left_packet=left_tail, right_packet=right_tail)
        else:
            print(f"{left_head} > {right_head}")
            return False

    # Check Case 3 (really a special case of Case 2).
    if isinstance(left_head, list) and isinstance(right_head, int):
        print("Case 3 triggered; converting right_head to list.")
        right_head = [right_head]
    elif isinstance(left_head, int) and isinstance(right_head, list):
        print("Case 3 triggered; converting left_head to list.")
        left_head = [left_head]

    # Check Case 2.
    print("Case 2 triggered: left_head and right_head are lists.")
    if left_tail and right_tail:
        print("Recursively check heads and tails.")
        return check_packets(left_packet=left_head, right_packet=right_head) and check_packets(left_packet=left_tail, right_packet=right_tail)
    else:
        print("Recursively check heads only.")
        return check_packets(left_packet=left_head, right_packet=right_head)

    # if isinstance(left, int) and isinstance(right, int):        # Case 1.
    #     return left < right
    # elif isinstance(left, list) and isinstance(right, list):    # Case 2.
    #     if left_index > len(left_packet) and right_index < len(right_packet):
    #         return False    # Right ran out before left; packets are not in order.
    #     return check_packets(left_packet=left[0], right_packet=right[0], left_index=left_index + 1, right_index=right_index + 1) \
    #            and check_packets(left_packet=left[1:], right_packet=right[1:], left_index=left_index + 1, right_index=right_index + 1)
    # elif isinstance(left, list) and isinstance(right, int):     # Case 3.
    #     right = [right]
    #     # Apply Case 2.
    #     if left_index > len(left_packet) and right_index < len(right_packet):
    #         return False    # Right ran out before left; packets are not in order.
    #     right_packet[0] = right
    #     return     check_packets(left_packet=left[0], right_packet=right[0], left_index=0, right_index=0) \
    #            and check_packets(left_packet=left[1:], right_packet=right, left_index=left_index + 1, right_index=right_index + 1)
    # elif isinstance(left, int) and isinstance(right, list):     # Case 3.
    #     left = [left]
    #     # Apply Case 2.
    #     if left_index > len(left_packet) and right_index < len(right_packet):
    #         return False    # Right ran out before left; packets are not in order.
    #     left_packet[0] = left
    #     return     check_packets(left_packet=left, right_packet=right[1:], left_index=left_index + 1, right_index=right_index + 1) \
    #            and check_packets(left_packet=left, right_packet=right[1:], left_index=left_index + 1, right_index=right_index + 1)


testing = False
if testing:
    distress_signal = io.file_to_list("input/day-13-test-data.txt")
else:
    distress_signal = io.file_to_list("input/day-13-input.txt")

print("Advent of Code 2022 Day 13")
print("-------------------------")

i = 0
pair_index = 1
ordered_pair_index_sum = 0
while i < len(distress_signal) - 1:
    print(f"i: {i}")
    # All lines of distress_signal are valid Python lists.
    left_packet = eval(distress_signal[i])
    right_packet = eval(distress_signal[i + 1])
    print(f"left_packet: {left_packet}")
    print(f"right_packet: {right_packet}\n")

    # Now determine if the packet pair is in order.
    if check_packets(left_packet=left_packet, right_packet=right_packet):
        print("Current packet pair is in order.\n")
        ordered_pair_index_sum += pair_index
    else:
        print("Current packet pair is not in order.\n")

    i += 3
    pair_index += 1

print("PART 1")
print("======")
print(f"Sum of all ordered packet pairs: {ordered_pair_index_sum}")
print("======")
# Attempt 1: 2773 (too low)
