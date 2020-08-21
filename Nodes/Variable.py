from Nodes.Node import Node


class Variable(Node):
    def __init__(self, id, name, graph):
        super().__init__(id, name, graph)
        self.reversed = False
        self.deduce_visited = False
        self.evaluated = False

    def solve(self, query=None):
        if self.evaluated is True:
            return self.value, self.fixed

        self.evaluated = True
        name = self.name  # ! Operator handling

        try:
            if name[0] == '!':
                name = self.name[1:]
                self.reversed = True

            value, is_fixed = self.graph.db[name].solve(query)

            if value is not None:
                self.fixed = is_fixed
                self.evaluated = True
                self.value = value if self.reversed is False else not value
            else:
                self.value = value

            return self.value, self.fixed

        except KeyError:
            if self.reversed is True:
                return True, False
            else:
                return False, False
