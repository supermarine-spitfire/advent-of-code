from collections import deque

from lib import io

def check_packets(left_packet, right_packet):
    print("In check_packets().")
    print(f"left_packet: {left_packet}")
    print(f"right_packet: {right_packet}\n")
    # General algorithm:
    # Split left and right packets (each a deque) into two pieces each: call them head and tail.
    # The head is the first element of each packet deque; the tail, the remaining elements of the packet deques.
    # Check the heads of left and right according to the cases outlined below.
    # Recursively check the tails of left and right according to the cases outlined above.
    # AND the result of the head check with that of the tail check and return the result.
    #
    # Cases to consider for proper order:
    # 1. If both current elements are integers, the left one must be less than the right one for the packet pair to be in order.
    # 2. If both current elements are lists, recursively check each current element's values according to the cases defined herein.
    #    If the left element list runs out before the right element list, the packet pair is in order.
    # 3. If exactly one of the elements is an integer, convert that integer to a list and apply Case 2.

    # When the packets contain nested lists, the state of the packet search (i.e. what is left in both packet deques
    # before going into the list) is pushed onto the packet_states deque.
    packet_states = deque()

    # The left packet controls everything under the ordering scheme defined above: hence loop over it.
    while left_packet:
        if not right_packet:    # Case 2 base sub-case.
            print("Case 2 triggered; right ran out first.")
            return False        # Right ended before left; hence out of order.

        print(f"packet_states: {packet_states}")
        left_head = left_packet.popleft()
        right_head = right_packet.popleft()
        left_tail = left_packet
        right_tail = right_packet
        print(f"left_head: {left_head}")
        print(f"right_head: {right_head}")
        print(f"left_tail: {left_tail}")
        print(f"right_tail: {right_tail}")
        # Check Case 1.
        if isinstance(left_head, int) and isinstance(right_head, int):
            print("Case 1 triggered: left_head and right_head are integers.")
            if left_head < right_head:
                print(f"{left_head} < {right_head}")
                return True
            elif left_head == right_head:
                print(f"{left_head} = {right_head}: check tails of packets.")
                # Check if tails are empty.
                if not left_packet:
                    if not right_packet:
                        # Tails are empty; pop most recent packet state and iterate from there.
                        print("Case 2 triggered: both ran out at same time.")
                        print("Restoring most recent packet state.")
                        left_head, right_head = packet_states.pop()
                        left_packet = left_head
                        right_packet = right_head
                        print(f"left_head: {left_head}")
                        print(f"right_head: {right_head}")
                        continue
                    print("Case 2 triggered: left ran out first.")
                    return True     # Left ended before right; hence in order.
                elif not right_packet: 
                    print("Case 2 triggered: right ran out first.")
                    return False    # Right ended before left; hence out of order.
                print("Both full: moving to next elements.")
                continue    # Tails are full; move on to next element.
            else:
                print(f"{left_head} > {right_head}")
                return False

        # Check Case 3 (really a special case of Case 2).
        if isinstance(left_head, list) and isinstance(right_head, int):
            print("Case 3 triggered; converting right_head to deque.")
            print(f"right_head (before conversion): {right_head}")
            d = deque()
            d.append(right_head)
            right_head = d
            print(f"right_head (after conversion): {right_head}")
        elif isinstance(left_head, int) and isinstance(right_head, list):
            print("Case 3 triggered; converting left_head to deque.")
            print(f"left_head (before conversion): {left_head}")
            d = deque()
            d.append(left_head)
            left_head = d
            print(f"left_head (after conversion): {left_head}")

        # Handle Case 2.
        print("Case 2 triggered: left_head and right_head are lists.")
        print("Pushing current packet state onto packet_states.")
        packet_states.append((left_tail, right_tail))
        print(f"packet_states: {packet_states}")
        left_head = left_head if isinstance(left_head, deque) else deque(left_head)
        right_head = right_head if isinstance(right_head, deque) else deque(right_head)
        print(f"Now iterating on left_head ({left_head}), right_head ({right_head}) lists.")
        left_packet = left_head
        right_packet = right_head


    print("Case 2 triggered; left ran out first or both ran out at same time.")
    return True # Left ended before right; hence in order.


    # These conditions check if Case 2's base sub-case is triggered.
    # if len(left_packet) == 0:
    #     print("Case 2 triggered; left ran out first or both ran out at same time.")
    #     return True     # A tentative true value; following recursive calls may cancel it out.
    # elif len(right_packet) == 0:
    #     print("Case 2 triggered; right ran out first.")
    #     return False    # Right ended before left: hence out of order.

    # Split packets into their heads and tails.
    # left_head = left_packet[0]
    # right_head = right_packet[0]
    # left_tail = left_packet[1:]
    # right_tail = right_packet[1:]
    # print(f"left_head: {left_head}")
    # print(f"right_head: {right_head}")
    # print(f"left_tail: {left_tail}")
    # print(f"right_tail: {right_tail}")
    # if len(left_packet) > 1:
    #     left_tail = left_packet[1:]
    # if len(right_packet) > 1:
    #     right_tail = right_packet[1:]

    # Check Case 1.
    # if isinstance(left_head, int) and isinstance(right_head, int):
    #     print("Case 1 triggered: left_head and right_head are integers.")
    #     if left_head < right_head:
    #         print(f"{left_head} < {right_head}")
    #         return True
    #     elif left_head == right_head:
    #         print(f"{left_head} = {right_head}: recursively check tails of packets.")
    #         return check_packets(left_packet=left_tail, right_packet=right_tail)
    #     else:
    #         print(f"{left_head} > {right_head}")
    #         return False

    # Check Case 3 (really a special case of Case 2).
    # if isinstance(left_head, list) and isinstance(right_head, int):
    #     print("Case 3 triggered; converting right_head to list.")
    #     right_head = [right_head]
    # elif isinstance(left_head, int) and isinstance(right_head, list):
    #     print("Case 3 triggered; converting left_head to list.")
    #     left_head = [left_head]

    # Check Case 2.
    # print("Case 2 triggered: left_head and right_head are lists.")
    # if left_tail and right_tail:
    #     print("Recursively check heads and tails.")
    #     return check_packets(left_packet=left_head, right_packet=right_head) and check_packets(left_packet=left_tail, right_packet=right_tail)
    # else:
    #     print("Recursively check heads only.")
    #     return check_packets(left_packet=left_head, right_packet=right_head)


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
    # All lines of distress_signal are valid Python lists. Make them into deques.
    left_packet = deque(eval(distress_signal[i]))
    right_packet = deque(eval(distress_signal[i + 1]))
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
# Attempt 2: 6216 (too high)
# Attempt 3: 6134 (too high)
