import networkx as nx

def build_satellite_network(satellite_names):
    """
    Build a graph representing satellite communication network.
    Args:
        satellite_names: List of satellite names from TLE data
    Returns:
        nx.Graph: Graph with satellites as nodes and communication links as edges
    """
    G = nx.Graph()
    G.add_nodes_from(satellite_names)
    # Create edges between all pairs (simplified for small networks)
    for i, name1 in enumerate(satellite_names):
        for name2 in satellite_names[i+1:]:
            G.add_edge(name1, name2)
    return G

def get_best_route(G, source, dest):
    """
    Find the shortest communication path between two satellites.
    Args:
        G: NetworkX graph
        source: Source satellite name
        dest: Destination satellite name
    Returns:
        list: Shortest path or empty list if no path exists
    """
    try:
        return nx.shortest_path(G, source, dest)
    except nx.NetworkXNoPath:
        return []
