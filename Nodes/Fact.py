from Nodes.Node import Node


class Fact(Node):
    """Node with fixed value True"""

    def __init__(self, id, name, graph):
        super().__init__(id, name, graph)
        self.value = True
        self.fixed = True

    def solve(self, query=None):
        return True, True
