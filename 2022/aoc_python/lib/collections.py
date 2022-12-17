import sys

from abc import abstractclassmethod
from collections import deque
from enum import Enum
from queue import PriorityQueue


class Vertex:
    class Colour(Enum):
        # Used for breadth-first search.
        BLACK = 0   # Discovered vertex.
        GREY = 1    # "Frontier" between discovered and undiscovered vertices.
        WHITE = 2   # Undiscovered vertex.

    def __init__(self, label, data):
        self.label = label
        self.data = data

        self.predecessor = None # Reference to another Vertex; used for graph searches.
        self.colour = None      # Label used for graph searches.
        self.distance = None    # Tracks smallest number of edges from a source Vertex to self.

    def __hash__(self) -> int:
        return hash(self.label)

    def __eq__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.label == other.label
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.label < other.label
        return False

    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, Vertex):
            return self.label > other.label
        return False

    def __ge__(self, other) -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __str__(self) -> str:
        return   f"Vertex(label: {self.label}, data: {self.data}, " \
               + f"predecessor: ({self.predecessor.label if self.predecessor else None}, " \
               + f"{self.predecessor.data if self.predecessor else None}), " \
               + f"colour: {self.colour}, " \
               + f"distance: {self.distance})"

    __repr__ = __str__


class Graph:
    def __init__(self):
        self.adjacency_lists = {}
        self.vertices = []

    def __str__(self) -> str:
        s = f"Vertices: {sorted(self.vertices)}"+ "\nAdjacency lists:\n"
        for vertex, edges in self.adjacency_lists.items():
            s += f"({vertex.label}, {vertex.data}): {edges}\n"
        return s

    __repr__ = __str__

    @abstractclassmethod
    def add_vertex(self, v):
       pass

    @abstractclassmethod
    def remove_vertex(self, v):
        pass

    def get_vertex(self, label):
        # Returns None if no vertices have the provided label.
        for v in self.vertices:
            if v.label == label:
                return v
        return None

    def vertex_in_graph(self, label):
        return label in map(lambda v: v.label, self.vertices)

    @abstractclassmethod
    def add_edge(self, source, target):
        pass

    @abstractclassmethod
    def remove_edge(self, source, target):
        pass

    def is_adjacent(self, source, target):
        return target in self.adjacency_lists[source]

    def neighbours(self, v):
        return set(self.adjacency_lists[v]) if v in self.adjacency_lists.keys() else set()

    def reset_vertices(self):
        for v in self.vertices:
            v.colour = None
            v.distance = None
            v.predecessor = None

    def clear(self):
        self.adjacency_lists = {}
        self.vertices = []

    def bfs(self, source):
        # Implements breadth-first search.
        # print("In Graph.bfs().")
        # print(f"self before initialisation: {self}")
        if not self.vertex_in_graph(source.label):
            return False

        for v in self.vertices:
            v.colour = Vertex.Colour.WHITE  # Unvisited.
            v.distance = sys.maxsize        # Effectively infinitely far from source.
            v.predecessor = None
            # print(f"v: {v}")
        vertices = self.vertices.copy()
        vertices.remove(source)
        # print(f"vertices: {sorted(vertices)}")
        # print(f"self after initialisation: {self}")

        source.colour = Vertex.Colour.GREY  # Visited by default; has neighbouring unvisited vertices.
        source.distance = 0
        source.predecessor = None
        # print(f"source: {source}\n")

        vertices_to_process = deque()
        vertices_to_process.append(source)
        while vertices_to_process:
            # print(f"vertices_to_process (before loop): {vertices_to_process}")
            u = vertices_to_process.popleft()
            # print(f"u: {u}")
            neighbours = self.neighbours(u)
            # print(f"neighbours: {neighbours}")
            for v in neighbours:
                # print(f"v (neighbour of u): {v}")
                # print(f"v.colour: {v.colour}")
                if v.colour == Vertex.Colour.WHITE: # v has not been visited yet.
                    v.colour = Vertex.Colour.GREY   # Add to frontier; there may be neighbouring unvisited vertices.
                    v.distance = u.distance + 1
                    v.predecessor = u
                    # print(f"v discovered: {v}. Will process.")
                    vertices_to_process.append(v)
            u.colour = Vertex.Colour.BLACK          # All neighbouring vertices have been visited.
            # print(f"All neighbours of {u} discovered.")
            # print(f"vertices_to_process (after loop): {vertices_to_process}\n")
        # print("Vertices after search:")
        # for v in sorted(self.vertices):
            # print(f"v: {v}")

        return True


class DirectedGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_vertex(self, v):
        # Returns the original vertex or a reference to a copy of it already in the graph, if present.
        if v not in self.vertices:
            self.adjacency_lists[v]= set()
            self.vertices.append(v)
            return v
        else:
            return self.vertices[self.vertices.index(v)]

    def remove_vertex(self, v):
        # Returns boolean flag indicating if operation succeeded or not.
        if v in self.vertices:
            del self.adjacency_lists[v]
            self.vertices.remove(v)
            return v
        else:
            return False

    def add_edge(self, source, target):
        # Returns boolean flag indicating if operation succeeded or not.
        if source not in self.vertices or target not in self.vertices:
            return False
        elif source in self.adjacency_lists.keys():
            self.adjacency_lists[source].add(target)
            return True
        else:
            self.adjacency_lists[source] = set().add(target)
            return True

    def remove_edge(self, source, target):
        # Returns boolean flag indicating if operation succeeded or not.
        if source in self.adjacency_lists.keys():
            self.adjacency_lists[source].remove(target)
            return True
        else:
            return False

    def get_path(self, source, target, list_of_edges):
        if source == target:
            return [source]
        elif target.predecessor is None:
            return []
        else:
            return self.get_path(source, target.predecessor, list_of_edges.append(target))


class DirectedWeightedGraph(Graph):
    def __init__(self):
        self.edge_weights = {}
        super().__init__()

    def __str__(self) -> str:
        s = super().__str__() + "Edge weights:\n"
        for edge, weight in self.edge_weights.items():
            s += f"{edge}: {weight}\n"
        return s

    def add_vertex(self, v):
        # Returns the original vertex or a reference to a copy of it already in the graph, if present.
        if v not in self.vertices:
            self.adjacency_lists[v] = set()
            self.vertices.append(v)
            return v
        else:
            return self.vertices[self.vertices.index(v)]

    def remove_vertex(self, v):
        # Returns boolean flag indicating if operation succeeded or not.
        if v in self.vertices:
            del self.adjacency_lists[v]
            self.vertices.remove(v)
            return v
        else:
            return False

    def add_edge(self, source, target, weight):
        # Returns boolean flag indicating if operation succeeded or not.
        if source not in self.vertices or target not in self.vertices:
            return False
        elif source in self.adjacency_lists.keys():
            self.adjacency_lists[source].add(target)
            self.edge_weights[(source.label, target.label)] = weight
            return True
        else:
            self.adjacency_lists[source] = set().add(target)
            self.edge_weights[(source.label, target.label)] = weight
            return True

    def remove_edge(self, source, target):
        # Returns boolean flag indicating if operation succeeded or not.
        if source in self.adjacency_lists.keys() and target in self.adjacency_lists[source]:
            self.adjacency_lists[source].remove(target)
            if (source.label, target.label) in self.edge_weights.keys():
                del self.edge_weights[(source.label, target.label)]
            return True
        else:
            return False

    def update_edge(self, source, target, weight):
        # Returns boolean flag indicating if operation succeeded or not.
        if source not in self.vertices or target not in self.vertices:
            return False
        else:
            self.edge_weights[(source.label, target.label)] = weight
            return True

    def get_edge_weight(self, source, target):
        if source not in self.vertices or target not in self.vertices:
            return None
        else:
            return self.edge_weights[(source.label, target.label)]

    def clear(self):
        self.edge_weights = {}
        super().clear()

    def initialise_single_source(self, source):
        """Call before running shortest-path algorithms."""
        for v in self.vertices:
            v.distance = sys.maxsize    # Stand-in for infinity.
            v.predecessor = None
        source.distance = 0

    def relax(self, source, target):
        """Updates target.distance with the shortest path distance to target.

        Also sets source as target's predecessor if target.distance is updated.
        """
        if target.distance > source.distance + self.edge_weights[(source.label, target.label)]:
            target.distance = source.distance + self.edge_weights[(source.label, target.label)]
            target.predecessor = source

    def dijkstra(self, source):
        """Run's Dijkstra's algorithm for the single-source shortest-path problem."""
        self.initialise_single_source(source)
        final_vertices = set()  # Vertices whose final shortest-path weights from source are determined.
        vertices_to_process = PriorityQueue()
        for v in self.vertices:
            vertices_to_process.put((v.distance, v), block=False)    # Use distance value as priority.

        while not vertices_to_process.empty():
            u = vertices_to_process.get(block=False)[1] # Throw away priority value.
            # print(f"u: {u}")
            final_vertices.add(u)
            for v in self.neighbours(u):
                # print(f"v: {v}")
                self.relax(u, v)
            # print()
