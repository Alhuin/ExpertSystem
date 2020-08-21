from Nodes import Node
from errors import ParadoxError, CustomError


class Knowledge(Node):
    """Query node which value can be computed by solving its children or deducing from a deduction node"""

    def __init__(self, id, name, graph):
        super().__init__(id, name, graph)
        self.visited = True
        self.deduction_node_id = list()
        self.deduction_parsed: bool = False

    def print(self):
        print(f"\n{self.name} has value {self.value} {'(evaluated)' if self.evaluated is True else ''}")

    def solve(self, query=None):
        """Compute the query node value from children & deduction nodes"""

        results: list = list()
        print(f'\nKNOWLEDGE SOLVE: solving {self.name}')

        if self.fixed is True:
            print(f'KNOWLEDGE SOLVE: {self.name}: already solved: value = {self.value}, self_fixed = {self.fixed}')
            return self.value, self.fixed

        neighbors = list(self.graph.adj[self.id])

        # Solving children
        print(f'KNOWLEDGE SOLVE: {self.name}: solving implications')
        for neighbor in neighbors:
            n = self.graph.nodes[neighbor]['data']
            if n.name != '=':
                value, is_fixed = n.solve()
                results.append([value, is_fixed])

        print(f"KNOWLEDGE SOLVE: {self.name}: {len(results)} implications solved")
        print(results)

        children_value = False
        children_fixed = False

        # Computing children results
        for result in results:
            if result[1] is True:
                if children_fixed is False:
                    children_value = result[0]
                    children_fixed = result[1]
                elif children_fixed is True and result[0] != children_value:
                    self.contradiction = True
                    raise ParadoxError(self.name)
            elif result[0] is True and children_fixed is False:
                children_value = result[0]

        deduction_value = False
        deduction_fixed = False

        # Solving deduction nodes
        if len(self.deduction_node_id) != 0:
            for node_id in self.deduction_node_id:
                deduction_node = self.graph.nodes[node_id]['data']
                if deduction_node.deduction_parsed is False and deduction_node.name is not None and deduction_node.name != query:
                    print(f"KNOWLEDGE SOLVE: {self.name}: {deduction_node.name} not parsed yet, evaluating")
                    try:
                        deduction_node.deduce_from_expression()
                    except CustomError:
                        self.contradiction = True
                        raise ParadoxError(self.name)

            # Checking if deduction allowed to compute a new value for the query
            deduction_value = self.graph.db[self.name].value
            deduction_fixed = self.graph.db[self.name].fixed

            print(f"KNOWLEDGE SOLVE: deduction done new value = {deduction_value}, is_fixed = {deduction_fixed}")

        print(f"children: v = {children_value}, f = {children_fixed}")
        print(f"deduce: v = {deduction_value}, f = {deduction_fixed}")

        # Comparing results from children and deduction nodes
        if children_fixed is True:
            if deduction_fixed is True and deduction_value != children_value:
                raise ParadoxError(self.name)
            else:
                self.value = children_value
                self.fixed = children_fixed
        elif deduction_fixed is True:
            if children_fixed is True and children_value != deduction_value:
                raise ParadoxError(self.name)
            else:
                self.value = deduction_value
                self.fixed = deduction_fixed
        else:
            if children_value is True or deduction_value is True:
                self.value = True
            elif self.undetermined is True:
                return 'Undetermined', True

        return self.value, self.fixed

    def deduce_from_expression(self):
        """Try to deduce the value of the knowledges composing the query node"""

        print(f"KNOWLEDGE DEDUCE: evaluating {self.name}")
        self.deduction_parsed = True
        value, is_fixed = self.solve()
        print(f"KNOWLEDGE DEDUCE: {self.name} solved: value = {value}, is_fixed = {is_fixed}")
        if value is True:
            neighbors = list(self.graph.adj[self.id])

            print(f"KNOWLEDGE DEDUCE: {self.name}: asking deduction from children with value {value}")
            for neighbor in neighbors:
                n = self.graph.nodes[neighbor]['data']
                if n.name == '=' and n.deduce_parsed is False:
                    n.deduce_from_expression()

            for neighbor in neighbors:
                n = self.graph.nodes[neighbor]['data']
                if n.name == '=':
                    n.deduce_parsed = False

