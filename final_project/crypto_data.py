# crypto_data.py
# Sara Sezavar 
"""
Utility functions for:
(1) Fetching live crypto exchange rates from CoinGecko
(2) building a dictionary of currency pairs
(3) saving exchange-rate data inside the data/folder
"""

import requests
import json
from pathlib import Path
from datetime import datetime

# 13 cryptocurrencies (7 original + 6 additional)
COIN_IDS = [
    "ethereum",
    "bitcoin",
    "litecoin",
    "ripple",
    "cardano",
    "bitcoin-cash",
    "eos",
    "solana",
    "polkadot",
    "chainlink",
    "stellar",
    "tron",
    "dogecoin",
]

COIN_TICKERS = [
    "eth",
    "btc",
    "ltc",
    "xrp",
    "ada",
    "bch",
    "eos",
    "sol",
    "dot",
    "link",
    "xlm",
    "trx",
    "doge",
]

ID_TO_TICKER = {
    "ethereum": "eth",
    "bitcoin": "btc",
    "litecoin": "ltc",
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
    "solana": "sol",
    "polkadot": "dot",
    "chainlink": "link",
    "stellar": "xlm",
    "tron": "trx",
    "dogecoin": "doge",
}

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def fetch_prices_from_coingecko() -> dict:
    """Fetches crypto prices from the CoinGecko API and returns parsed JSON."""

    ids = ",".join(COIN_IDS)
    vs = ",".join(COIN_TICKERS)

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies={vs}"
    )

    print("Requesting live prices from CoinGecko API...")

    # Add User-Agent header because CoinGecko rejects anonymous/default requests
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    response.raise_for_status()
    data = json.loads(response.text)

    # debug output — helps diagnose empty API responses
    print("DEBUG: Raw CoinGecko response received.")
    print("DEBUG keys:", list(data.keys()))

    return data


def build_pairs_from_json(data: dict) -> dict:
    """Builds a dictionary of currency pair rates: pairs[(from, to)] = rate."""

    pairs = {}

    for coin_id, rates_dict in data.items():

        # Skip coins that returned empty data (usually due to rate limits)
        if not rates_dict:
            print(f"WARNING: CoinGecko returned empty rates for {coin_id}. Skipping.")
            continue

        from_sym = ID_TO_TICKER[coin_id]

        for to_sym, rate in rates_dict.items():
            if rate and rate > 0:
                pairs[(from_sym, to_sym)] = float(rate)

    # Debug print
    print(f"DEBUG: Total parsed pairs: {len(pairs)}")
    if pairs:
        print("DEBUG sample pairs:", list(pairs.items())[:5])

    return pairs


def save_pairs_to_file(pairs: dict) -> Path:
    """Saves currency-pair data to a timestamped text file inside data/."""
    
    # Windows-safe timestamp (no colon)
    ts = datetime.utcnow().strftime("%Y.%m.%d_%H.%M")
    filename = DATA_DIR / f"currency_pair_{ts}.txt"

    with filename.open("w", encoding="utf-8") as f:
        f.write("currency_from,currency_to,exchange_rate\n")
        for (src, dst), rate in pairs.items():
            f.write(f"{src},{dst},{rate}\n")

    print(f"Saved currency pairs to {filename}")
    return filename

