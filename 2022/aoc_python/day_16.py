import re

from lib import io
from lib.collections import DirectedWeightedGraph, Vertex

class ValveState:
    def __init__(self, flow_rate, is_open):
        self.flow_rate = flow_rate
        self.is_open = is_open

    def __eq__(self, other) -> bool:
        if isinstance(other, ValveState):
            return self.flow_rate == other.flow_rate and self.is_open == other.is_open
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"ValveState(flow_rate: {self.flow_rate}, is_open: {self.is_open})"

    __repr__ = __str__


print("Advent of Code 2022 Day 16")
print("-------------------------")

testing = True
if testing:
    valve_scan = io.file_to_list("input/day-16-test-data.txt")
else:
    valve_scan = io.file_to_list("input/day-16-input.txt")

# Load valve data.
valve_network = DirectedWeightedGraph()
valves = {}
for valve in valve_scan:
    cur_valve, target_valves = valve.split(";")
    cur_valve = cur_valve.split()
    cur_valve_label = cur_valve[1]
    flow_rate = int(cur_valve[-1].split("=")[-1])

    target_valves = [
        tv.rstrip(",") for tv in re.split(r"valves?", target_valves)[-1].split()
    ]
    valves[cur_valve_label] = (flow_rate, target_valves)

# print(f"valves: {valves}")

# Build valve vertices first.
for source_valve, data in valves.items():
    valve_vertex = Vertex(label=source_valve, data=ValveState(flow_rate=data[0], is_open=False))
    valve_network.add_vertex(valve_vertex)

# Connect valve vertices.
for source_valve, data in valves.items():
    # print(f"source_valve: {source_valve}")
    # print(f"data: {data}")
    source = valve_network.get_vertex(source_valve)
    targets = list(
        filter(
            # lambda v: v != None,
            lambda v: True,
            [valve_network.get_vertex(target_valve) for target_valve in data[1]]
        )
    )
    # print(f"targets: {targets}")
    for target in targets:
        valve_network.add_edge(source=source, target=target, weight=data[0])
print(valve_network)

# Algorithm for stepping across valves:
# Consider modifying A*, with the neighbour's neighbours' pressure as the heuristic.
# Starting at source valve ("AA"), mark it visited and pick the target valve that has the highest flow rate.
# Move to that target valve.
# Check neighbours of the target valve and their neighbors.
# If any have a higher flow rate than the current valve, move to the valve with the highest flow rate.
# Otherwise, open the valve.

print("PART 1")
print("======")
print(f": ")
print("======")
