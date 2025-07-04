#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:55:40 2025

@author: mohithsai
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class Exchange(Enum):
    """
    Supported stock exchanges and their Yahoo Finance suffixes:
    - NSE (National Stock Exchange): suffix "NS"
    - BSE (Bombay Stock Exchange): suffix "BO"
    """
    NSE = "NS"
    BSE = "BO"

    @classmethod
    def from_str(cls, s: str) -> "Exchange":
        """
        Parse a user string into an Exchange enum member.

        Args:
            s (str): e.g. "nse", "BSE" (case‑insensitive).
        Returns:
            Exchange: NSE or BSE.
        Raises:
            ValueError: if input is not one of the enum names.
        """
        key = s.strip().upper()
        if key not in cls.__members__:
            valid = ", ".join(cls.__members__)
            raise ValueError(f"Invalid exchange {s!r}; choose one of: {valid}")
        return cls[key]

@dataclass
class Trade:
    """
    Represents the optimal single buy/sell transaction.

    Attributes:
        buy_date  (datetime): When to buy.
        sell_date (datetime): When to sell.
        buy_price (float):    Purchase price.
        sell_price(float):    Sale price.
        profit    (float):    Net profit.
    """
    buy_date:  datetime
    sell_date: datetime
    buy_price: float
    sell_price: float
    profit:     float