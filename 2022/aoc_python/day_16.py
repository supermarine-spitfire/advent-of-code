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

def disconnect_zero_flow_valves(valve_network):
    print("In disconnect_zero_flow_valves().")
    # Create edges that bypass any zero-flow-rate valve vertices.
    for source_valve in valve_network.vertices:
        print(f"source_valve: {source_valve}")
        if source_valve.data.flow_rate == 0 and source_valve.label != "AA":
            continue    # Ignore this valve.

        for u in valve_network.neighbours(source_valve):
            print(f"\tu: {u}")
            if u.data.flow_rate == 0 and u.label != "AA":   # Treat AA separately.
                # Check if any neighbours of u can be connected to source_valve.
                for v in valve_network.neighbours(u):
                    if v == source_valve:   # Do not make cycles.
                        continue
                    print(f"\t\tv: {v}")
                    if v.data.flow_rate > 0 and v != source_valve:
                        print(f"\t\tBypassing {u.label} by connecting {source_valve.label} to {v.label}.")
                        # Bypass edge collapses 2 edges into 1; the weight reflects this.
                        valve_network.add_edge(source=source_valve, target=v, weight=2)

                        # Disconnect the zero-flow-rate valve.
                        valve_network.remove_edge(source=source_valve, target=u)
                        valve_network.remove_edge(source=u, target=v)

    # Since source valve AA has a flow rate of 0, remove all edges leading to it. Only keep edges leading out of AA.
    print("Now disconnecting other valves from AA.")
    for source_valve in valve_network.vertices:
        if source_valve.label == "AA":
            continue
        valve_network.remove_edge(source=source_valve, target=valve_network.get_vertex("AA"))


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

# Build valve vertices first.
for source_valve, data in valves.items():
    valve_vertex = Vertex(label=source_valve, data=ValveState(flow_rate=data[0], is_open=False))
    valve_network.add_vertex(valve_vertex)

# Connect valve vertices.
for source_valve, data in valves.items():
    source = valve_network.get_vertex(source_valve)
    targets = [valve_network.get_vertex(target_valve) for target_valve in data[1]]
    for target in targets:
        valve_network.add_edge(source=source, target=target, weight=1)

# print("\nvalve_network.vertices")
# for v in valve_network.vertices:
#     print(v)

# print("\nvalve_network.adjacency_lists")
# for k, v in valve_network.adjacency_lists.items():
#     print(f"{k}:")
#     for w in v:
#         print(f"\tlabel: {w.label}, distance: {w.distance}, data: {w.data}")

disconnect_zero_flow_valves(valve_network)
print("\nvalve_network.vertices")
for v in valve_network.vertices:
    print(v)

print("\nvalve_network.adjacency_lists")
for k, v in valve_network.adjacency_lists.items():
    print(f"{k}:")
    for w in v:
        print(f"\tlabel: {w.label}, distance: {w.distance}, data: {w.data}")

# Algorithm for stepping across valves:
# For each valve, run Dijkstra's algorithm to figure out the shortest distances from the current valve to all the other valves.
# Store these distances in dictionaries indexed by valve. These dictionaries are indexed by source valve.
# Start at the source valve, then apply the following algorithm:
# 1. Define a minute counter with a value of 1.
# 2. If the current valve has a non-zero flow rate, open it.
# 3. If the previous instruction was run, increment the minute counter.
# 4. Look at the current valve's neighbours. Ignoring any that have a zero flow rate, move to the valve with the highest flow rate.
# 5. Increment the minute counter.
distances = {}
for v in valve_network.vertices:
    valve_network.dijkstra(v)
    distances[v.label] = {w.label: w.distance for w in valve_network.vertices}

# print("distances:")
# for k, v in distances.items():
#     print(k, v)

# print("\nvalve_network.vertices")
# for v in valve_network.vertices:
#     print(v)

# print("\nvalve_network.adjacency_lists")
# for k, v in valve_network.adjacency_lists.items():
#     print(f"{k}:")
#     for w in v:
#         print(f"\tlabel: {w.label}, distance: {w.distance}, data: {w.data}")

print("PART 1")
print("======")
print(f": ")
print("======")
