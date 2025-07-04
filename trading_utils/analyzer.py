#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:58:50 2025

@author: mohithsai
"""

import pandas as pd
from trading_utils.types import Trade
class TradeAnalyzer:
    """
    Implements the O(n) single‑transaction max‑profit algorithm:
    track the lowest price seen so far and update best profit when
    encountering a higher price.
    """
    def find_best_trade(self, prices: pd.Series) -> Trade | None:
        """
        Args:
            prices (pd.Series): Date‑indexed closing prices.
        Returns:
            Trade or None if no positive profit is possible.
        """
        values    = prices.to_numpy()
        dates     = prices.index
        min_price = float('inf')
        min_date  = None
        best_profit = 0.0
        best_pair   = (None, None)

        for dt, raw in zip(dates, values):
            price = raw.item()       # numpy scalar → Python float
            profit = price - min_price
            if profit > best_profit:
                best_profit = profit
                best_pair   = (min_date, dt)
            if price < min_price:
                min_price = price
                min_date  = dt

        if best_profit <= 0:
            return None

        buy_dt, sell_dt = best_pair
        buy_price  = prices.loc[buy_dt].item()
        sell_price = prices.loc[sell_dt].item()

        return Trade(
            buy_date  = buy_dt,
            sell_date = sell_dt,
            buy_price = buy_price,
            sell_price= sell_price,
            profit    = best_profit
        )