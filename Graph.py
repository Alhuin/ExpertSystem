import networkx as nx
from Nodes import *
from errors import CustomError
from regex import operatorsRegex
import uuid


def generate_id():
    return uuid.uuid1()


class Graph(nx.Graph):
    db: dict = dict()

    def __init__(self, **attr):
        super().__init__(incoming_graph_data=None, **attr)

    def feed(self, parser):

        """ Create Knowledge nodes from facts and add them to graph and db with value True """

        for fact in parser.facts:
            self.add_knowledge(fact, None, True)

        """ Create Knowledge nodes from rules if they don't already exist and add them to graph and db """

        for rule in parser.rules:
            self.add_rule(rule)

        """ Find deductible knowledges from rules"""

        deducted_nodes = list()
        for rule in parser.rules:
            rule_str = rule[0]
            knowledge_str = rule[1]
            atoms = list(operatorsRegex.sub('', rule_str))
            atoms += list(operatorsRegex.sub('', knowledge_str))
            for atom in atoms:
                for k in self.db:
                    if atom in k and atom != k:
                        deducted_nodes.append([atom, self.db.get(k).id])

        """ Add deduction_nodes_id to knowledges, create knowledge if not in db """

        for node in deducted_nodes:
            self.add_knowledge(node[0], node[1])

    def add_knowledge(self, name, deduction_id=None, is_fact=False):
        root_id = generate_id()
        try:
            root_knowledge = self.db[name]
            root_id = root_knowledge.id
        except KeyError:
            root_knowledge = Knowledge(root_id, name, self) if is_fact is False else Fact(root_id, name, self)
            self.db[name] = root_knowledge

        if deduction_id is not None and isinstance(self.db[name], Fact) is False:
            self.db[name].deduction_node_id.append(deduction_id)

        self.add_node(root_id, data=self.db[name])
        return root_id

    def add_rule(self, rule, side='right'):
        composed = False
        reversed = False
        biconditional = False
        str = rule[1] if side == 'right' else rule[0]
        left = rule[2]
        right = rule[4]
        rel = rule[3]

        expression = right if side == 'right' else left

        if expression[0] == 'not':
            reversed = True
            if expression[1][0] == 'atom':
                knowledge = expression[1][1]
            else:
                knowledge = str[1:]
                composed = True
        elif expression[0] == 'atom':
            knowledge = expression[1]
        else:
            knowledge = str
            composed = True
        root_id = self.add_knowledge(knowledge)

        if rel == "<=>":
            biconditional = True if side == 'right' else False

        rel_id = generate_id()
        relation = "=>" if reversed is False else "!=>"
        implication = Implication(rel_id, relation, self)
        self.add_node(rel_id, data=implication)
        self.add_edge(root_id, rel_id)
        self.feed_ordered_elements(left if side == 'right' else right, rel_id)

        """ Create decomposition implication, represented by = """

        if composed is True:
            rel_id = generate_id()
            relation = "="
            implication = Implication(rel_id, relation, self)
            self.add_node(rel_id, data=implication)
            self.add_edge(root_id, rel_id)
            self.feed_ordered_elements(expression, rel_id, True)

        if biconditional is True:
            self.add_rule(rule, left)

    def feed_ordered_elements(self, left, root_id, composed=False):
        if left[0] == "not":
            if left[1][0] == "atom":
                var_id = generate_id()
                variable = Variable(var_id, f"!{left[1][1]}", self)
                self.add_node(var_id, data=variable)
                self.add_edge(root_id, var_id)
            elif left[1][0] == "operation":
                print(left[1])
                self.add_operation(left[1], root_id, True if composed is False else False)
            elif left[1][0] == "not":
                print(f"{left}")
                print(f"double not : {left[1]}")
                print(f"sening {left[1][1]}")
                self.feed_ordered_elements(left[1][1], root_id, composed)
        elif left[0] == "atom":
            var_id = generate_id()
            variable = Variable(var_id, left[1], self)
            self.add_node(var_id, data=variable)
            self.add_edge(root_id, var_id)
        elif left[0] == "operation":
            self.add_operation(left, root_id)
        elif left[0] == "parenthesis":
            print(left[1])
            self.feed_ordered_elements(left[1], root_id)

    def add_operation(self, left, root_id, reversed=False):
        operand_one = left[1]
        operator = left[2] if reversed is False else f"!{left[2]}"
        operand_two = left[3]
        operation_id = generate_id()
        operation = Operation(operation_id, operator, self)
        self.add_node(operation_id, data=operation)
        self.add_edge(root_id, operation_id)
        self.feed_ordered_elements(operand_one, operation_id)
        self.feed_ordered_elements(operand_two, operation_id)

    def solve(self, query):
        try:
            query_node = self.db[query]
            return query_node.solve()
        except CustomError:
            raise CustomError
