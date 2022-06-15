class Vertex:
    def __init__(self, id):
        self.id = id

class Edge:
    def __init__(self, first, second, directed = False):
        self.first = first
        self.second = second

class Graph:
    def __init__(self, edges: list[Edge]):
        self.edges = edges

