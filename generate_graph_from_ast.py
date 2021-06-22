import matplotlib.pyplot as plt
import networkx as nx
from tree_sitter import Language, Parser

PY_LANGUAGE = Language('/home/c402/PycharmProjects/pythonProject3/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)


def parse_py(node):
    if node == None:
        return
    print(node.type)
    for child in node.children:
        parse_py(child)


def parse_tree(code, parent_node, node, G):
    if node == None:
        return G
    # solve string print("hello world")
    if node.type == 'string':
        G.add_edge(parent_node.type, node.type)
        G.add_edge(node.type, code[node.children[0].start_byte + 1: node.children[-1].end_byte - 1])
        return G
    if parent_node and node:
        node_1 = parent_node.type
        node_2 = node.type
        if node_1 == 'identifier':
            node_1 = code[parent_node.start_byte:parent_node.end_byte]
        if node_2 == 'identifier':
            node_2 = code[node.start_byte:node.end_byte]
        G.add_edge(node_1, node_2)
    # print(stri+str(node.type))
    # stri += '    '

    for child in node.children:
        G = parse_tree(code, node, child, G)
    return G


if __name__ == '__main__':
    code = '''
    def add(x,y):
        return x+y
    print("hello world")
    '''

    tree = parser.parse(bytes(code, "utf8"))
    # print(tree.root_node.children[0])
    parse_py(tree.root_node)
    # print(tree.root_node)
    # print(tree.root_node.children)
    # print(tree.root_node.children[0].children)
    # print(tree.root_node.children[0].children[0].start_byte)
    G = nx.Graph()
    Gr = parse_tree(code, None, tree.root_node, G)
    print(list(G.edges))
    print(list(G.nodes)[1])
    #nx.draw(Gr, with_labels=True, font_weight='bold')
    #plt.show()
