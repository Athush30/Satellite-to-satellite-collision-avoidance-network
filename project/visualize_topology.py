import networkx as nx
import matplotlib.pyplot as plt
from routing import build_satellite_network

def visualize():
    G = build_satellite_network()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_weight='bold')
    plt.title("Satellite Communication Topology")
    plt.show()
