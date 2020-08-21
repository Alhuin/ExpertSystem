import uuid
from errors import CustomError
from Nodes.Variable import Variable
from Nodes import Node, Knowledge
from Operations import AND, OR, XOR


class Operation(Node):
    def __init__(self, id, name, graph):
        super().__init__(id, name, graph)
        self.reversed = name[0] == '!'
        self.operator = name if self.reversed is False else name[1:]
        self.deduce_visited = False

    def solve(self):
        if self.visited is True:
            return self.value, self.fixed
        self.visited = True

        operands = list()
        neighbors = list(self.graph.adj[self.id])

        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if n.visited is False:
                if isinstance(n, Variable) is True:
                    value, is_fixed = n.solve()
                else:
                    value, is_fixed = n.solve()
                operands.append([value, is_fixed])

        try:
            if self.operator == '+':
                self.value = AND(operands[0][0], operands[1][0]).run()
            elif self.operator == '|':
                self.value = OR(operands[0], operands[1]).run()
            elif self.operator == '^':
                self.value = XOR(operands[0], operands[1]).run()

            if self.value is None:
                self.value = False
            elif operands[0][1] is True and operands[1][1] is True:
                self.fixed = True
            elif operands[0][1] is True or operands[1][1] is True and self.operator == '|':
                self.fixed = True
            if self.reversed is True:
                self.value = not self.value
            return self.value, self.fixed
        except KeyError:
            return None

    def deduce_from_expression(self):
        self.deduce_visited = True
        operands = list()
        neighbors = list(self.graph.adj[self.id])
        values = []

        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if n.deduce_visited is False:
                operands.append(n)

        if self.operator == '+':
            for ope in operands:
                if isinstance(ope, Variable):
                    reversed = False
                    name = ope.name
                    if name[0] == '!':
                        reversed = True
                        name = ope.name[1:]
                    try:
                        node = self.graph.db[name]
                    except KeyError:
                        id = uuid.uuid1()
                        node = Knowledge(id, ope.name, self)
                        self.graph.db[node.name] = node
                        self.graph.add_node(id, data=node)
                    value = True if reversed is False else False
                    self.graph.db[name].evaluated = True
                    self.graph.db[name].value = value
                    self.graph.db[name].fixed = True
            for ope in operands:
                if isinstance(ope, Operation):
                    ope.deduce_from_expression()

        elif self.operator == '^':
            values = []
            for ope in operands:
                if isinstance(ope, Variable):
                    reversed = False
                    name = ope.name
                    if name[0] == '!':
                        reversed = True
                        name = ope.name[1:]
                    value = self.graph.db[name].solve()
                    if value[1] is False:
                        value = None
                    else:
                        value = value[0]
                    values.append(value if reversed is False else not value)
                else:
                    ope.deduce_composed_expression(True)

                deduced_true = None
                deduced_false = None

                if values == [True, True] or values == [False, False]:
                    raise CustomError
                if values == [None, False]:
                    deduced_true = operands[0]
                elif values == [None, True]:
                    deduced_false = operands[0]
                elif values == [False, None]:
                    deduced_true = operands[1]
                elif values == [True, None]:
                    deduced_false = operands[1]

                if deduced_true is not None:
                    reversed = False
                    name = deduced_true.name
                    if name[0] == '!':
                        reversed = True
                        name = deduced_true.name[1:]
                    value = True if reversed is False else False
                    self.graph.db[name].value = value
                    self.graph.db[name].fixed = True

                    print(f"\033[32mOPE DEDUCE: {self.name}: {name}, set to {value}\033[0m")

                elif deduced_false is not None:
                    reversed = False
                    name = deduced_false.name
                    if name[0] == '!':
                        reversed = True
                        name = deduced_false.name[1:]
                    value = False if reversed is False else True
                    self.graph.db[name].value = value
                    self.graph.db[name].fixed = True

                    print(f"\033[32mOPE DEDUCE: {self.name}: {name}, set to {value}\033[0m")

        elif self.operator == '|':
            for ope in operands:
                if isinstance(ope, Variable):
                    reversed = False
                    name = ope.name
                    if name[0] == '!':
                        reversed = True
                        name = ope.name[1:]
                    value = self.graph.db[name].solve()
                    value = value[0] if value[1] is True else None
                    values.append(value if reversed is False else not value)
            for ope in operands:
                if isinstance(ope, Operation):
                    values.append(ope.deduce_from_expression())

            deduced_knowledges = []
            undetermined = []
            if values == [None, None]:
                undetermined = operands
            if values == [False, False]:
                raise CustomError
            if values == [False, None]:
                deduced_knowledges.append(operands[1])
            elif values == [None, False]:
                deduced_knowledges.append(operands[0])

            for deduced in deduced_knowledges:
                reversed = False
                name = deduced.name
                if name[0] == '!':
                    reversed = True
                    name = deduced.name[1:]
                self.graph.db[name].value = True if reversed is False else False
                self.graph.db[name].fixed = True
                self.graph.db[name].evaluated = True

            for u in undetermined:
                name = u.name
                if u.name[0] == '!':
                    name = u.name[1:]
                self.graph.db[name].undetermined = True

                print(u.name, 'is undetermined')
