import sys

from enum import Enum
from queue import Queue

class Graph:
    def __init__(self):
        self.adjacency_lists = {}
        self.vertices = []

    def __str__(self) -> str:
        return f"""Vertices: {sorted(self.vertices)}
Adjacency lists: {self.adjacency_lists}
"""

    __repr__ = __str__

    def add_vertex(self, v):
        # Returns boolean flag indicating if operation succeeded or not.
        if v not in self.vertices:
            self.adjacency_lists[v]= set()
            self.vertices.append(v)
            return True
        else:
            return False

    def remove_vertex(self, v):
        # Returns boolean flag indicating if operation succeeded or not.
        if v in self.vertices:
            del self.adjacency_lists[v]
            self.vertices.remove(v)
            return True
        else:
            return False

    def get_vertex(self, label):
        # Returns None if no vertices have the provided label.
        for v in self.vertices:
            if v.label == label:
                return v
        return None

    def vertex_in_graph(self, label):
        return label in map(lambda v: v.label, self.vertices)

    def add_edge(self, source, target):
        # Returns boolean flag indicating if operation succeeded or not.
        if source not in self.vertices:
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

    def is_adjacent(self, source, target):
        return target in self.adjacency_lists[source]

    def neighbours(self, v):
        return set(self.adjacency_lists[v]) if v in self.adjacency_lists.keys() else set()

    def bfs(self, source):
        # Implements breadth-first search.
        print("In Graph.bfs().")
        if not self.vertex_in_graph(source.label):
            return False

        vertices = self.vertices.copy()
        vertices.remove(source)
        print(f"vertices: {vertices}")
        for v in vertices:
            v.colour = Vertex.Colour.WHITE
            v.distance = sys.maxsize
            v.predecessor = None
        
        source.colour = Vertex.Colour.GREY
        source.distance = 0
        source.predecessor = None

        vertices_to_process = Queue()
        vertices_to_process.put(source)
        while not vertices_to_process.empty():
            u = vertices_to_process.get()
            for v in self.neighbours(u):
                if v.colour == Vertex.Colour.WHITE: # v has not been visited yet.
                    v.colour = Vertex.Colour.GREY # Add to frontier; there may be neighbouring unvisited vertices.
                    v.distance = u.distance + 1
                    v.predecessor = u
                    vertices_to_process.put(v)
            u.colour = Vertex.Colour.BLACK # All neighbouring vertices have been visited.

        return True

    def get_path(self, source, target, list_of_edges=[]):
        if source == target:
            return [source]
        elif target.predecessor is None:
            return []
        else:
            return self.get_path(source, target.predecessor, list_of_edges.append(target))


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
            return f"Vertex({self.label}, {self.data})"

        __repr__ = __str__
