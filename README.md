# India Stocks Best Single Trade

A command‑line Python tool to fetch five years of historical closing prices for Indian equities (NSE/BSE) and compute the single best buy/sell pair to maximize profit.

---

## 🔍 Overview

`India Stocks Best Single Trade` is designed for analysts, quants, and traders who want a quick, accurate way to identify the optimal single‑transaction profit opportunity over the past five years for any Indian ticker symbol.

Key features:

* **5‑Year Lookback**: Automatically computes the exact date five years ago and rolls forward up to five trading days if that date is a holiday/weekend.
* **Exchange Agnostic**: Supports both NSE (`.NS`) and BSE (`.BO`) tickers via a simple prompt.
* **O(n) Profit Scan**: Implements the classic single‑transaction maximum profit algorithm in linear time.
* **Production‑Grade**: Includes logging, robust error handling, and clear user messaging.

---

## ⚙️ Prerequisites

Ensure you have Python 3.9+ installed along with:

```bash
pip install yfinance pandas python‑dateutil
```

---

## 📁 Project Structure

```plaintext
├── best_trade.py        # Main Python script (entry point)
├── trading_utils/       # Module containing core classes
│   ├── __init__.py      # Package init
│   ├── fetcher.py       # StockDataFetcher class
│   └── analyzer.py      # TradeAnalyzer class
├── README.md            # This documentation
└── requirements.txt     # Pinned dependencies
```

---

## 🚀 Installation

1. **Clone the repo**:

   ```bash
   ```

git clone [https://github.com/your-org/india-stocks-best-trade.git](https://github.com/your-org/india-stocks-best-trade.git)
cd india-stocks-best-trade

````

2. **Set up environment**:
   ```bash
pip install -r requirements.txt
````

3. **Verify**:

   ```bash
   ```

python best\_trade.py --help

````

---

## 🎯 Usage

Run the script and follow prompts:

```bash
python best_trade.py
````

1. **Enter ticker symbol** (e.g. `TCS`, `BEL`).
2. **Choose exchange**: `NSE` or `BSE`.

Example:

```
Enter ticker symbol (e.g. TCS, BEL): TCS
Exchange [NSE/BSE]: NSE
```

Output:

```
BEST TRADE for TCS.NS:
  • Buy  on 2020‑07‑06 at ₹2,150.00
  • Sell on 2025‑07‑01 at ₹4,380.00
  → Profit: ₹2,230.00
```

---

## 🏗️ Architecture & Code Overview

### 1. `Exchange` Enum

* Defines supported exchanges (`NSE`, `BSE`) and their Yahoo Finance suffixes (`NS`, `BO`).
* Factory method `from_str()` to parse user input.

### 2. `StockDataFetcher`

* **Responsibilities**:

  * Compute the exact date 5 years ago using `dateutil.relativedelta`.
  * Download OHLC data via `yfinance`.
  * Roll forward up to 5 days if the anniversary date is not a trading day.
  * Validate data presence and return a `pandas.Series` of closing prices.

* **Key Constants**:

  * `YEARS_BACK = 5`
  * `MAX_ROLL_DAYS = 5`

### 3. `TradeAnalyzer`

* **Responsibility**: Implements an O(n) scan to find the buy date with the lowest price and, concurrently, the sell date that maximizes profit.
* **Algorithm**:

  1. Initialize `min_price` = ∞, `best_profit` = 0.
  2. For each `(date, price)`:

     * Calculate `profit = price - min_price`.
     * Update `best_profit`, `buy_date`, and `sell_date` if `profit > best_profit`.
     * Update `min_price` if `price < min_price`.
  3. Return a `Trade` dataclass or `None` if no profit.

### 4. `Trade` Dataclass

* Encapsulates a single optimal transaction:

  * `buy_date`, `sell_date` (timestamps)
  * `buy_price`, `sell_price`, `profit` (floats)

### 5. `best_trade.py` (Main Script)

* **Flow**:

  1. Prompt user for ticker & exchange.
  2. Instantiate `StockDataFetcher`, retrieve closes.
  3. Instantiate `TradeAnalyzer`, compute trade.
  4. Print formatted result or "no profit" message.

* **Logging**:

  * Configured via `logging.basicConfig` to show timestamps and INFO‐level messages.

---

## 🛡️ Error Handling

* **No Data**: Raises a `ValueError` if Yahoo Finance returns empty or missing the `Close` column.
* **Roll Limit Exceeded**: Alerts if no trading day within 5 days after the 5-year anniversary.
* **NaN Cleanup**: Ensures all NaNs are dropped, or errors out if the resulting series is empty.

---

## 🔧 Extensibility

* **Lookback Period**: Change `YEARS_BACK` in `StockDataFetcher`.
* **Roll Logic**: Adjust `MAX_ROLL_DAYS` or add backward‑roll support.
* **Batch Mode**: Adapt the main script to process multiple tickers in a loop or via a file.

---

## 📜 License

MIT License. Feel free to fork and customize.

---

*Developed by \[Mohith Sai Gorla] — happy trading!*
