"""
------------------------------------------------------------------
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW8-Hard
------------------------------------------------------------------
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations


############################################################
# STEP 1: define the function
def count_high_degree_nodes(graph: nx.Graph) -> int:
    """
    Returns the number of nodes in the given NetworkX graph
    whose total degree (in + out) is greater than 5.
    """
    return sum(1 for node, degree in graph.degree() if degree > 5)


############################################################
# STEP 2: Create a sample graph to test the function
currencies = ["usd", "eur", "gbp", "mxn", "rub", "inr"]
edges = []

# Create weighted edges for all currency pairs
for c1, c2 in permutations(currencies, 2):
    rate = round((hash(c1 + c2) % 100) / 10 + 0.5, 2)
    edges.append((c1, c2, rate))

g = nx.DiGraph()
g.add_weighted_edges_from(edges)


############################################################
# STEP 3  call the function and display results
count = count_high_degree_nodes(g)
print("All nodes in the graph:", list(g.nodes))
print("Number of nodes with degree > 5:", count)


############################################################
# STEP 4 : Save the graph visualization
curr_dir = os.path.dirname(__file__)
graph_visual_fil = curr_dir + "/" + "hard_graph_visual.png"

pos = nx.circular_layout(g)
nx.draw_networkx(g, pos, node_color="lightgreen", with_labels=True)
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
plt.savefig(graph_visual_fil)
