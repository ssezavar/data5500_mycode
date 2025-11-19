"""
------------------------------------------------------------------
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
HW9: Crypto Currency Exchange Trading
------------------------------------------------------------------
"""

import requests
import json
import networkx as nx
from itertools import combinations
from itertools import permutations

# top 7 crypto currencies
ids = "ethereum,bitcoin,litecoin,ripple,cardano,bitcoin-cash,eos"
vs = "eth,btc,ltc,xrp,ada,bch,eos"

url = (
    "https://api.coingecko.com/api/v3/simple/price"
    f"?ids={ids}&vs_currencies={vs}"
)

print("Requesting live prices from CoinGecko API...")
response = requests.get(url)
data = json.loads(response.text)

# Mapping id → ticker
id_to_ticker = {
    "ethereum": "eth",
    "bitcoin": "btc",
    "litecoin": "ltc",
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos"
}

# ----------------------------------------------------------
# build graph
# ----------------------------------------------------------
g = nx.DiGraph()
edges = []

for coin_id in data:
    from_sym = id_to_ticker[coin_id]        # e.g. "eth"
    rates_dict = data[coin_id]              # e.g. {"btc":0.03, "eth":1, ...}

    for to_sym, rate in rates_dict.items():
        if rate > 0:
            edges.append((from_sym, to_sym, rate))

g.add_weighted_edges_from(edges)

print("\nGraph nodes:", g.nodes)
print("Graph edges:", g.edges)

# ----------------------------------------------------------
# traverse all possible paths and compute arbitrage
# ----------------------------------------------------------

min_factor = float("inf")
max_factor = float("-inf")
min_paths = None
max_paths = None

print("\n================ ARBITRAGE CHECK ================")

for n1, n2 in combinations(g.nodes, 2):

    # all possible paths from n1→n2
    for path_to in nx.all_simple_paths(g, source=n1, target=n2):

        # Compute forward weight
        w_to = 1.0
        for i in range(len(path_to)-1):
            w_to *= g[path_to[i]][path_to[i+1]]["weight"]

        # reverse path (n2→n1)
        path_from = list(reversed(path_to))
        w_from = 1.0
        for i in range(len(path_from)-1):
            w_from *= g[path_from[i]][path_from[i+1]]["weight"]

        factor = w_to * w_from

        print("\nPaths from", n1, "to", n2)
        print("Forward :", path_to, w_to)
        print("Reverse :", path_from, w_from)
        print("Factor  :", factor)

        # track min/max arbitrage factor
        if factor < min_factor:
            min_factor = factor
            min_paths = (path_to, path_from)

        if factor > max_factor:
            max_factor = factor
            max_paths = (path_to, path_from)

# ----------------------------------------------------------
# th final report
# ----------------------------------------------------------
print("\n================ RESULTS ================")
print("Smallest Path Weight Factor:", min_factor)
print("Paths:", min_paths)

print("\nGreatest Path Weight Factor:", max_factor)
print("Paths:", max_paths)
