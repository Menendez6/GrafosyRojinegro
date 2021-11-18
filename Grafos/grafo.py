import matplotlib.pyplot as plt
import networkx as nx 

G=nx.Graph()
G.add_node('A')
G.add_nodes_from(['B','C','D','E','F'])
G.add_edges_from([('A','B'),('B','C')])
G.add_edges_from([('C','E'),('E','D')])
G.add_edges_from([('C','F'),('F','G')])

nx.draw_circular(G,with_labels=True)
plt.show()

