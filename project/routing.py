import networkx as nx

def build_satellite_network():
    G = nx.Graph()
    G.add_nodes_from(["SAT1", "SAT2"])
    G.add_edges_from([
        ("SAT1", "SAT2")
    ])
    return G

def get_best_route(G, source, dest):
    try:
        return nx.shortest_path(G, source, dest)
    except nx.NetworkXNoPath:
        return []
