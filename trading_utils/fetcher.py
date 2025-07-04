#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:58:11 2025

@author: mohithsai
"""

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd
from trading_utils.types import Exchange

logger = logging.getLogger(__name__)

class StockDataFetcher:
    """
    Downloads 5 years of historical closing prices for a given ticker+exchange,
    rolling forward up to 5 calendar days if the exact anniversary falls
    on a non‑trading day.
    """
    YEARS_BACK    = 5  # lookback period in years
    MAX_ROLL_DAYS = 5  # max days to roll forward from anniversary

    def __init__(self, exchange: Exchange):
        """
        Args:
            exchange (Exchange): NSE or BSE enum value.
        """
        self.exchange = exchange

    def fetch_closes(self, ticker: str) -> pd.Series:
        """
        Fetches and returns a pandas Series of closing prices.

        1. Builds full ticker (e.g. "TCS.NS").
        2. Computes target date = today − YEARS_BACK.
        3. Downloads OHLC data via yfinance.
        4. Rolls forward to next trading day within MAX_ROLL_DAYS.
        5. Returns clean Series of 'Close'.

        Args:
            ticker (str): Stock symbol, no suffix.
        Raises:
            ValueError on missing data, no trading day, or all NaNs.
        """
        full_tkr = f"{ticker}.{self.exchange.value}"
        today    = datetime.today()
        target   = today - relativedelta(years=self.YEARS_BACK)

        logger.info(f"Downloading {full_tkr} from {target.date()} to {today.date()}")
        df = yf.download(
            full_tkr,
            start=target.strftime("%Y-%m-%d"),
            end  =today.strftime("%Y-%m-%d"),
            progress=False,
            auto_adjust=False
        )

        # Validate presence of data and Close column
        if df.empty or 'Close' not in df.columns:
            raise ValueError(f"No closing price data for {full_tkr}")

        # Ensure chronological order
        df = df.sort_index()

        # Roll forward to first trading day ≥ target
        valid = df.index[df.index >= target]
        if valid.empty:
            raise ValueError(f"No trading days on/after {target.date()}")
        start_date = valid[0]

        # Check roll‑forward limit
        delta = (start_date.date() - target.date()).days
        if delta > self.MAX_ROLL_DAYS:
            raise ValueError(
                f"First trading day {start_date.date()} is more than "
                f"{self.MAX_ROLL_DAYS} days after {target.date()}"
            )

        closes = df.loc[start_date:, 'Close'].dropna()
        if closes.empty:
            raise ValueError("All fetched closing prices are NaN.")
        return closes