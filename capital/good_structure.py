import networkx as nx
from capital.trade_utils import AMT_AVAIL
# import matplotlib.pyplot as plt


class GoodStruct:

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_node(self, node):
        self.G.add_node(node)

    def add_edge(self, node1, node2, weight=None):
        '''
        add an edge between node1 and node2
        '''
        self.G.add_edge(node1, node2, weight=weight)

    def draw_graph(self):
        nx.draw_shell(self.G, with_labels=True, font_weight='bold')

        # pos = graphviz_layout(self.G)
        # plt.axis('off')
        # nx.draw_networkx_nodes(self.G,pos,node_color='g',alpha = 0.8)
        # nx.draw_networkx_edges(self.G,pos,edge_color='b',alpha = 0.6)
        # nx.draw_networkx_edge_labels(self.G,pos,edge_labels = \
        # nx.get_edge_attributes(self.G,'weight'))
        # nx.draw_networkx_labels(self.G,pos) # node lables

        # plt.savefig('graph.png')

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

    def get_weight(self, node1, node2):
        '''
        get weight of the edge between node1 and node2
        '''
        return self.G[node1][node2][0]['weight']

    def max_neighbors(self, node, goods):
        '''
        Iterate over neighbors in a breadth-first-search starting at node,
        and return the max of the weights
        '''
        ls_neighbors = self.neighbors(node)
        ls_weights = {}
        for i in ls_neighbors:
            if goods[i][AMT_AVAIL]:
                ls_weights[i] = self.get_weight(node, i)
        max_util_node = max(ls_weights, key=ls_weights.get)
        return ls_weights[max_util_node]


def main():
    goods = GoodStruct()
    goods.add_node("pizza base")
    goods.add_node("oven")
    goods.add_node("land")
    goods.add_node("refrigerator")
    goods.add_node("cheese")
    goods.add_node("peperoni")
    goods.add_node("lamp")
    goods.add_node("sun light")

    goods.add_edge("land", "oven", weight=2)
    goods.add_edge("oven", "land", weight=4)
    goods.add_edge("land", "refrigerator", weight=4)
    goods.add_edge("refrigerator", "land", weight=4)

    goods.add_edge("cheese", "refrigerator", weight=4)
    goods.add_edge("peperoni", "refrigerator", weight=4)
    goods.add_edge("pizza base", "oven", weight=4)
    goods.add_edge("pizza base", "peperoni", weight=2)
    goods.add_edge("pizza base", "cheese", weight=2)
    goods.add_edge("land", "lamp", weight=1)
    goods.add_edge("sun light", "lamp", weight=-4)
    goods.add_edge("land", "sun light", weight=1)

    print("node:", goods.nodes(), "\n")
    print("edges:", goods.edges(), "\n")
    print("number of nodes:", len(goods), "\n")
    print("graph as a string:", goods, "\n")
    print("neighbors of piazza:", goods.neighbors("pizza base"), "\n")

    print("weight from land to oven:", goods.get_weight('land', 'oven'))
    print("weight from oven to land:", goods.get_weight('oven', 'land'))

    print("weight from refrigerator to land:",
          goods.get_weight('refrigerator', 'land'))
    print("weight from land to refrigerator:",
          goods.get_weight('land', 'refrigerator'))

    print("weight from \'sun light' to \'lamp':",
          goods.get_weight("sun light", "lamp"))

    print(goods.max_neighbors("land"))

    goods.draw_graph()


if __name__ == '__main__':
    main()
