#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:59:32 2025

@author: mohithsai
"""

import logging
from trading_utils.types     import Exchange
from trading_utils.fetcher   import StockDataFetcher
from trading_utils.analyzer  import TradeAnalyzer

# Configure root logger for INFO‑level with timestamps
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """
    1) Prompt user for ticker and exchange.
    2) Fetch 5 years of closing prices.
    3) Compute best single-trade profit.
    4) Print formatted result.
    """
    ticker_in = input("Enter ticker symbol (e.g. TCS, BEL): ").strip().upper()
    exch_in   = input("Exchange [NSE/BSE]: ").strip().upper()
    exchange  = Exchange.from_str(exch_in)

    fetcher = StockDataFetcher(exchange)
    closes  = fetcher.fetch_closes(ticker_in)

    analyzer  = TradeAnalyzer()
    trade     = analyzer.find_best_trade(closes)

    if trade is None:
        print(
            f"No profitable trade found for {ticker_in}.{exchange.value} "
            f"in the last {fetcher.YEARS_BACK} years."
        )
    else:
        b, s = trade.buy_date.date(), trade.sell_date.date()
        print(f"BEST TRADE for {ticker_in}.{exchange.value}:")
        print(f"  • Buy  on {b} at ₹{trade.buy_price:.2f}")
        print(f"  • Sell on {s} at ₹{trade.sell_price:.2f}")
        print(f"  → Profit: ₹{trade.profit:.2f}")

if __name__ == "__main__":
    main()