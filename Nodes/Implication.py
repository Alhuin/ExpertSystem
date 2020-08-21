from Nodes import Node, Knowledge


class Implication(Node):
    """ The first children of a query node solution """
    def __init__(self, id, name, graph):
        super().__init__(id, name, graph)
        self.visited = True
        self.deduce_visited = True
        self.deduce_parsed = False

    def solve(self):
        """ Compute children nodes of the solution, returns False, False (False by default) if the value is False"""
        print(f"\nIMP SOLVE:")
        neighbors = self.graph.neighbors(self.id)
        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if isinstance(n, Knowledge) is False:
                print(f"IMP SOLVE: solving neighbor {n.name}")
                value, is_fixed = n.solve()
                print(f"\nIMP SOLVE: {n.name} solved: value = {value}, fixed ? {is_fixed}")
                if self.name[0] == '!' and value is False:
                    return False, False
                if value is False:
                    return value, is_fixed
                self.value = not value if self.name[0] == '!' else value
                self.fixed = is_fixed
                return self.value, self.fixed

    def deduce_from_expression(self):

        print(f"IMP DEDUCE:")
        neighbors = self.graph.neighbors(self.id)
        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if isinstance(n, Knowledge) is False:
                print(f"IMP DEDUCE: aking deduction to neighbor {n.name}")
                n.deduce_from_expression()
                self.deduce_parsed = True

        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if isinstance(n, Knowledge) is False:
                n.deduce_visited = False