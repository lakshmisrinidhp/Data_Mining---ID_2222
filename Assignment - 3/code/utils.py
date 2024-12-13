import random
import networkx as nx

def reservoir_sampling(stream, k):
    
    reservoir = []
    for i, edge in enumerate(stream):
        if i < k:
            reservoir.append(edge)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = edge
    return reservoir

def count_wedges_and_closed_wedges(reservoir):
   
    subgraph = nx.Graph()
    subgraph.add_edges_from(reservoir)

    wedge_count = 0
    closed_wedge_count = 0

    for node in subgraph.nodes():
        neighbors = list(subgraph.neighbors(node))
        num_neighbors = len(neighbors)
        if num_neighbors < 2:
            continue
        wedges = [(neighbors[i], neighbors[j]) for i in range(num_neighbors) for j in range(i + 1, num_neighbors)]
        wedge_count += len(wedges)
        for u, v in wedges:
            if subgraph.has_edge(u, v):
                closed_wedge_count += 1

    return wedge_count, closed_wedge_count

def estimate_transitivity(wedge_count, closed_wedge_count):
    
    if wedge_count == 0:
        return 0
    return (3 * closed_wedge_count) / wedge_count
