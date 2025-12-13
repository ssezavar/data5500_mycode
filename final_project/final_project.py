"""
--------------------------------------------------------------------------------------
Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
--------------------------------------------------------------------------------------
Final Project: Crypto Currency Trading
This program:
1) Fetches live crypto exchange rates from CoinGecko (JSON API)
2) Saves currency pair data into data/currency_pair_YYYY.MM.DD:HH.MM.txt
3) Builds a directed graph using NetworkX and analyzes all possible paths
4) Computes forward and reverse path weights and identifies arbitrage opportunities
5) Sends paper-trading orders to Alpaca for top opportunities
6) Saves a final summary in results.json
--------------------------------------------------------------------------------------
"""

from crypto_data import (
    fetch_prices_from_coingecko,
    build_pairs_from_json,
    save_pairs_to_file,
)
from graph_analysis import build_graph_from_pairs, analyze_arbitrage
    # No changes or addition required 
from alpaca_client import paper_trade_opportunities
from utils_fp import save_results


def main():
    # 1) fetch live data from CoinGecko
    prices_json = fetch_prices_from_coingecko()

    # 2) build currency pair dictionary
    pairs = build_pairs_from_json(prices_json)

    # 3) Save raw pair data into the data/ folder
    data_file = save_pairs_to_file(pairs)

    # 4) Build the graph for analysis
    g = build_graph_from_pairs(pairs)

    # 5) Run arbitrage analysis
    analysis_result = analyze_arbitrage(g, min_profitable_factor=1.001)

    # 6) submit paper-trading orders to Alpaca for top opportunities
    opportunities = analysis_result.get("opportunities", [])
    trade_results = paper_trade_opportunities(
        opportunities,
        max_trades=3,
        notional_usd=10.0,
    )

    # 7) build summary and save to results.json
    results_summary = {
        "num_pairs": len(pairs),
        "data_file": str(data_file),
        "min_factor": analysis_result["min_factor"],
        "min_paths": analysis_result["min_paths"],
        "max_factor": analysis_result["max_factor"],
        "max_paths": analysis_result["max_paths"],
        "num_opportunities": len(opportunities),
        "trades_executed": trade_results,
    }

    save_results(results_summary)

    print("\nFinal project run completed.")


if __name__ == "__main__":
    main()
