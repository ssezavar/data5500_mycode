"""
------------------------------------------------------------------
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW8-Easy
------------------------------------------------------------------
"""

import os
import networkx as nx
import matplotlib.pyplot as plt


############################################################
# STEP 1 - Define the function
def count_nodes(graph: nx.Graph) -> int:
    """
    Returns the total number of nodes in the given NetworkX graph.
    """
    return graph.number_of_nodes()


############################################################
# STEP 2 - Create a sample graph to test the function
currencies = ["usd", "eur", "gbp"]

# Each edge represents an exchange rate between two currencies
edges = [
    ("usd", "eur", 0.92),
    ("eur", "usd", 1.09),
    ("usd", "gbp", 0.78),
    ("gbp", "usd", 1.28),
    ("eur", "gbp", 0.85),
    ("gbp", "eur", 1.17)
]

g = nx.DiGraph()
g.add_weighted_edges_from(edges)


############################################################
# STEP 3 - Call the function and display results
num_nodes = count_nodes(g)
print("All nodes in the graph:", list(g.nodes))
print("Number of nodes in the graph:", num_nodes)


############################################################
# STEP 4 - Save the graph visualization
curr_dir = os.path.dirname(__file__)
graph_visual_fil = curr_dir + "/" + "easy_graph_visual.png"

pos = nx.circular_layout(g)
nx.draw_networkx(g, pos, node_color="lightblue", with_labels=True)
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
plt.savefig(graph_visual_fil)
