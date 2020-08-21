class Node:
    """Parent class for all nodes in the graph"""

    def __init__(self, id, name, graph):
        self.id: hex = id
        self.name: str = name
        self.graph = graph
        self.value: bool = False
        self.visited: bool = False
        self.fixed: bool = False
        self.contradiction: bool = False
        self.undetermined: bool = False

