# graph_analysis.py
# Sara Sezavar 
"""
Builds the crypto graph and performs arbitrage analysis:
- Builds a directed graph (DiGraph) from currency pairs
- Finds all simple paths between every pair of nodes
- Computes forward and reverse path weights and factor = w_to * w_from
"""

import networkx as nx
from itertools import combinations


def build_graph_from_pairs(pairs: dict) -> nx.DiGraph:
    """
    Builds a directed NetworkX graph from a dictionary of currency pairs.
    pairs: dict[(from_symbol, to_symbol)] = rate
    """
    g = nx.DiGraph()
    edges = [(src, dst, rate) for (src, dst), rate in pairs.items()]
    g.add_weighted_edges_from(edges)
    return g


def analyze_arbitrage(g: nx.DiGraph, min_profitable_factor: float = 1.001) -> dict:
    min_factor = float("inf")
    max_factor = float("-inf")
    min_paths = None
    max_paths = None

    opportunities = []

    print("\nRunning arbitrage analysis (optimized)...")

    for n1, n2 in combinations(g.nodes, 2):

        # cutoff=3 makes it fast & still useful
        for path_to in nx.all_simple_paths(g, source=n1, target=n2, cutoff=3):

            w_to = 1.0
            for i in range(len(path_to) - 1):
                w_to *= g[path_to[i]][path_to[i + 1]]["weight"]

            path_from = list(reversed(path_to))
            w_from = 1.0
            for i in range(len(path_from) - 1):
                w_from *= g[path_from[i]][path_from[i + 1]]["weight"]

            factor = w_to * w_from

            if factor < min_factor:
                min_factor = factor
                min_paths = (path_to, path_from)

            if factor > max_factor:
                max_factor = factor
                max_paths = (path_to, path_from)

            if factor > min_profitable_factor:
                opportunities.append(
                    {
                        "from": n1,
                        "to": n2,
                        "path_to": path_to,
                        "path_from": path_from,
                        "w_to": w_to,
                        "w_from": w_from,
                        "factor": factor,
                    }
                )

    print("\nArbitrage analysis complete.")
    print(f"Total opportunities: {len(opportunities)}")

    return {
        "min_factor": min_factor,
        "min_paths": min_paths,
        "max_factor": max_factor,
        "max_paths": max_paths,
        "opportunities": opportunities,
    }
