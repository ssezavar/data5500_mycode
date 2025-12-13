# alpaca_client.py
# Sara Sezavar 
"""
Utility functions for sending paper-trading crypto orders to Alpaca.
Note:
- Requires an active Alpaca paper trading account
- Requires environment variables:
    APCA_API_KEY_ID
    APCA_API_SECRET_KEY
"""

import os
import requests

ALPACA_API_KEY_ID = os.environ.get("APCA_API_KEY_ID")
ALPACA_API_SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY")

BASE_URL = "https://paper-api.alpaca.markets"  # must remain paper trading URL

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY_ID or "",
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY or "",
    "Content-Type": "application/json",
}

# Mapping from our internal tickers to Alpaca trading symbols (<TICKER>USD)
TICKER_TO_SYMBOL = {
    "btc": "BTCUSD",
    "eth": "ETHUSD",
    "ltc": "LTCUSD",
    "xrp": "XRPUSD",
    "ada": "ADAUSD",
    "bch": "BCHUSD",
    "eos": "EOSUSD",
    "sol": "SOLUSD",
    "dot": "DOTUSD",
    "link": "LINKUSD",
    "xlm": "XLMUSD",
    "trx": "TRXUSD",
    "doge": "DOGEUSD",
}


def submit_crypto_order(symbol: str, side: str, notional_usd: float = 10.0) -> dict:
    """
    Submits a market order to Alpaca using a notional USD amount.
    side: 'buy' or 'sell'
    """
    if not ALPACA_API_KEY_ID or not ALPACA_API_SECRET_KEY:
        print("WARNING: Alpaca API keys not set. Skipping order submission.")
        return {"status": "skipped_no_keys"}

    url = f"{BASE_URL}/v2/orders"
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "market",
        "time_in_force": "gtc",
        "notional": str(notional_usd),
    }

    print(f"Submitting {side} order for {symbol} (notional ${notional_usd})")

    response = requests.post(url, headers=HEADERS, json=payload, timeout=20)

    if response.status_code >= 400:
        print("Order failed:", response.status_code, response.text)
        return {"status": "error", "code": response.status_code, "body": response.text}

    data = response.json()
    print("Order submitted:", data.get("id", "no_id"))
    return {"status": "ok", "order": data}


def paper_trade_opportunities(
    opportunities: list,
    max_trades: int = 3,
    notional_usd: float = 10.0
) -> list:
    """
    Places paper trades for a limited number of arbitrage opportunities.
    Simplified logic:
        - Buy the first coin in the forward path
        - Sell the last coin in the forward path
    This is not a real arbitrage execution model but is sufficient
    for demonstrating paper trading in the final project.
    """
    trade_results = []
    count = 0

    # Sort opportunities by highest arbitrage factor first
    for opp in sorted(opportunities, key=lambda x: x["factor"], reverse=True):
        if count >= max_trades:
            break

        path_to = opp["path_to"]
        first_ticker = path_to[0]
        last_ticker = path_to[-1]

        sym_buy = TICKER_TO_SYMBOL.get(first_ticker)
        sym_sell = TICKER_TO_SYMBOL.get(last_ticker)

        # skip unsupported coins on Alpaca
        if not sym_buy or not sym_sell:
            continue

        # submit buy and sell orders
        res_buy = submit_crypto_order(sym_buy, "buy", notional_usd=notional_usd)
        res_sell = submit_crypto_order(sym_sell, "sell", notional_usd=notional_usd)

        trade_results.append(
            {
                "factor": opp["factor"],
                "path_to": path_to,
                "path_from": opp["path_from"],
                "buy_symbol": sym_buy,
                "sell_symbol": sym_sell,
                "buy_result": res_buy,
                "sell_result": res_sell,
            }
        )

        count += 1

    return trade_results
