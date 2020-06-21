import networkx as nx
import pylab as plt


class GoodStruct:

    def __init__(self):
        self.G = nx.Graph()

    def add_node(self, node):
        self.G.add_node(node)

    def add_edge(self, node1, node2):
        '''
        add an edge between node1 and node2
        '''
        self.G.add_edge(node1, node2)

    def draw_graph(self):
        nx.draw_shell(self.G, with_labels=True, font_weight='bold')
        plt.savefig('graph.png')

    def __str__(self):
        return str(self.nodes())

    def __repr__(self):
        return str(self.G)

    def __len__(self):
        '''
        return the number of nodes in the graph
        '''
        return self.G.order()

    def nodes(self):
        '''
        return the list of all nodes in the graph
        '''
        return self.G.nodes()

    def edges(self):
        return self.G.edges()

    def neighbors(self, node):
        '''
        list all the neighbors for node in the graph
        '''
        return list(self.G.neighbors(node))

    def remove(self, node):
        '''
        remove node from graph
        '''
        self.G.remove_node(node)


def main():
    goods = GoodStruct()
    goods.add_node("pizza base")
    goods.add_node("oven")
    goods.add_node("land")
    goods.add_node("refrigerator")
    goods.add_node("cheese")
    goods.add_node("peperoni")

    goods.add_edge("land", "oven")
    goods.add_edge("land", "refrigerator")
    goods.add_edge("cheese", "refrigerator")
    goods.add_edge("peperoni", "refrigerator")
    goods.add_edge("pizza base", "oven")
    goods.add_edge("pizza base", "peperoni")
    goods.add_edge("pizza base", "cheese")

    print("node:", goods.nodes(), "\n")
    print("edges:", goods.edges(), "\n")
    print("number of nodes:", len(goods), "\n")
    print("graph as a string:", goods, "\n")
    print("neighbors of piassa:", goods.neighbors("pizza base"), "\n")
    goods.draw_graph()


if __name__ == '__main__':
    main()
