# India Stocks Best Single Trade

A command‑line Python tool to fetch five years of historical closing prices for Indian equities (NSE/BSE) and compute the single best buy/sell pair to maximize profit.

---

## 🔍 Overview

`India Stocks Best Single Trade` is tailored for traders, quants, and financial analysts seeking a robust, automated way to identify the optimal single‑transaction profit opportunity over the past five years, specifically for Indian stock tickers on NSE or BSE.

Key features:

* **5‑Year Lookback**: Calculates the exact date five years prior and rolls forward up to five trading days if that date falls on a weekend or market holiday.
* **Exchange Support**: Prompt‑driven support for NSE (`.NS`) and BSE (`.BO`) symbols.
* **O(n) Efficiency**: Leverages a linear‑time algorithm to find the maximum profit buy/sell pair in a single pass.
* **Production‑Ready**: Includes structured logging, comprehensive error handling, and clear user messaging.

---

## ⚙️ Prerequisites

* Python 3.9 or higher
* Internet connection to fetch data from Yahoo Finance

Install required packages:

```bash
pip install yfinance pandas python-dateutil
```

---

## 📁 Repository Structure

```plaintext
├── best_trade.py         # Main CLI entrypoint
├── trading_utils/        # Core library modules
│   ├── __init__.py       # Package initialization
│   ├── types.py          # Exchange enum & Trade dataclass
│   ├── fetcher.py        # StockDataFetcher implementation
│   └── analyzer.py       # TradeAnalyzer implementation
├── README.md             # Project documentation
└── requirements.txt      # Pinned dependencies
```

---

## 🚀 Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/iammohith/Single-Buy-Sell-Algorithm-For-Indian-Stocks.git \
     && cd Single-Buy-Sell-Algorithm-For-Indian-Stocks
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation** (optional):

   ```bash
   python best_trade.py --help
   ```

---

## 🎯 Usage

Run the script and follow the interactive prompts:

```bash
python best_trade.py
```

1. **Enter ticker symbol** (e.g., `TCS`, `BEL`).
2. **Select exchange** by typing `NSE` or `BSE`.

**Example session**:

```text
Enter ticker symbol (e.g. TCS, BEL): BEL
Exchange [NSE/BSE]: NSE
```

**Sample output**:

```text
BEST TRADE for BEL.NS:
  • Buy  on 2020-10-29 at ₹28.88
  • Sell on 2025-07-01 at ₹432.25
  → Profit: ₹403.37
```

---

## 🏗️ Architecture & Code Overview

### 1. `trading_utils.types`

* **`Exchange` Enum**: Maps `NSE`/`BSE` to Yahoo Finance suffixes `.NS`/`.BO`, with input parsing via `from_str()`.
* **`Trade` Dataclass**: Encapsulates buy/sell dates, prices, and profit.

### 2. `trading_utils.fetcher` (`StockDataFetcher`)

* **Responsibilities**:

  * Compute `target_date = today - 5 years` using `relativedelta`.
  * Download OHLC data via `yfinance` for `ticker.exchange`.
  * Roll forward up to 5 calendar days if `target_date` is non‑trading.
  * Validate and return a cleaned `pandas.Series` of closing prices.
* **Key Constants**:

  * `YEARS_BACK = 5`
  * `MAX_ROLL_DAYS = 5`

### 3. `trading_utils.analyzer` (`TradeAnalyzer`)

* **Responsibility**: Implements a single‑pass O(n) scan to identify the optimal buy/sell dates.
* **Algorithm**:

  1. Initialize `min_price = ∞`, `best_profit = 0`.
  2. Iterate through `(date, price)`:

     * Compute `profit = price - min_price`.
     * Update `best_profit` and record `buy_date` & `sell_date` if improved.
     * Update `min_price` if `price` is lower.
  3. Return a `Trade` instance or `None` if no positive profit.

### 4. `best_trade.py` (CLI)

* **Flow**:

  1. Prompt for ticker & exchange via stdin.
  2. Fetch closing prices with `StockDataFetcher`.
  3. Analyze with `TradeAnalyzer`.
  4. Print results or a “no profit” message.
* **Logging**: Configured with `logging.basicConfig` at INFO level.

---

## 🛡️ Error Handling

* **Data Unavailable**: Raises `ValueError` if Yahoo Finance returns empty data or missing the `Close` column.
* **Roll Window Exceeded**: Errors if no trading day within 5 days of the 5‑year anniversary.
* **NaN Purge**: Drops NaNs, errors if the resulting series is empty.

---

## 🔧 Customization & Extensibility

* Modify `YEARS_BACK` or `MAX_ROLL_DAYS` in `StockDataFetcher` for different lookback periods or roll logic.
* Extend batch processing by looping over multiple tickers or reading from a CSV.
* Integrate with scheduling tools (cron, Airflow) for automated runs.

---

## 📜 License

MIT License. Contributions and forks are welcome.

---

*Developed by Mohith Sai Gorla — happy trading!*
