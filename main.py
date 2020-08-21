import sys
import networkx as nx
import matplotlib.pyplot as plt
from Parser import Parser
from Graph import Graph
from errors import CustomError, ParadoxError
from Nodes import *


def get_node_properties(G):
    color: list = list()
    size: list = list()

    for node in G.nodes():
        n = G.nodes[node]['data']
        if isinstance(n, Knowledge):
            color.append('#33ccff')
            size.append(1500)
        elif isinstance(n, Fact):
            color.append('chartreuse')
            size.append(1500)
        else:
            size.append(500)
        if isinstance(n, Operation):
            color.append('cyan')
        elif isinstance(n, Implication) is True:
            if n.name[0] == '!':
                color.append('tomato')
            elif n.name == '=':
                color.append('chartreuse')
            elif n.name == '=>':
                color.append('lime')
        elif isinstance(n, Variable) is True:
            color.append('pink')
    return color, size


def get_edge_labels(G):
    ret = dict()
    for (u, v) in G.edges():
        rel = ret[(u, v)] = G.get_edge_data(u, v)['rel']
        if '=' not in rel:
            ret[(u, v)] = rel
        else:
            ret[(u, v)] = ''
    return ret


def get_edge_colors(u, v, G):
    rel = G.get_edge_data(u, v)['rel']
    if rel == '!=>':
        return 'red'
    elif rel == '=':
        return 'chartreuse'
    return 'black'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error : Please enter only one argument")
        exit(0)

    G = Graph()
    data = open(sys.argv[1], "r")
    lines = data.readlines()

    if lines:
        try:
            # Parse lines
            p = Parser(lines)
            p.run()
            p.print()

            # Feed graph
            G.feed(p)
        except SyntaxError:
            print("Error : Wrong Syntax")
            exit(0)

        # Prepare graph to be drawn
        pos = nx.spring_layout(G, scale=5)
        plt.figure()
        node_labels = dict([(node, G.nodes[node]['data'].name) for node in G.nodes])
        node_colors, node_sizes = get_node_properties(G)

        nx.draw(G, pos, with_labels=True, width=1, linewidths=1, node_size=node_sizes,
                node_color=node_colors, alpha=0.9, labels=node_labels, edge_color='black')

        # Solve Queries
        try:
            for query in p.queries:
                for node in G.nodes():
                    n = G.nodes[node]['data']
                    n.undetermined = False
                    n.contradiction = False
                    if isinstance(n, Variable):
                        n.visited = False
                    elif isinstance(n, Operation):
                        n.visited = False
                        n.deduce_visited = False
                    elif isinstance(n, Knowledge):
                        n.deduction_parsed = False
                    elif isinstance(n, Variable):
                        n.deduce_visited = False
                        n.reversed = False
                        n.evaluated = False
                try:
                    value, is_fixed = G.solve(query)
                    print(f"\n# solution {query} = {value}\n")
                except KeyError:
                    print(f"# solution {query} = False")
                except ParadoxError as p:
                    print(f"# solution {query} = Error : Contradiction for the fact", p.fact)
                    exit(0)
                    # continue

        except CustomError as e:
            pass

        # Draw Graph
        # plt.axis('off')
        # plt.show()


