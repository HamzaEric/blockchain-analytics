# Blockchain Analytics

A structured, multi-page Streamlit application designed to categorize, track, and analyze cryptocurrencies across live market prices, macro fundamentals, and quantitative correlations.

This tool bridges the gap between traditional price speculation and actual on-chain utility by overlaying market data with network usage metrics.

## Features

* ** Home:** Overview of tracked assets categorized by sector (e.g., Layer 1s, Stablecoins, DeFi, Privacy) and project methodology.
* ** Prices & Metrics (`1_Prices_Metrics.py`):** Fetches live price data, market capitalization, and volume via `yfinance`. Features interactive charts with adjustable timeframes and 50/200-day Simple Moving Averages.
* ** Network Fundamentals (`2_Fundamentals.py`):** Ingests static on-chain datasets (exported from DeFiLlama) to visualize macro trends like Total Value Locked (TVL) across chains, DEX volume dominance, and global stablecoin liquidity.
* ** Quantitative Correlations (`3_Correlations.py`):** A correlation engine that merges live historical price data with native on-chain metrics (e.g., Solana historical TVL). It calculates the Pearson Correlation Coefficient to determine if an asset's price is driven by fundamental network usage.

## Project Structure

Make sure your directory matches the following structure for the app to route pages and locate datasets correctly:

```text
blockchain-analytics/
│
├── home.py                 # Main entry point and overview page
├── requirements.txt        # Python dependencies
│
├── Datafiles/              # Local directory containing exported CSV datasets
│   ├── chains TVL.csv
│   ├── dex-volumes.csv
│   ├── stablecoins.csv
│   ├── stablecoins-chains.csv
│   └── solana.csv          
│
└── pages/                  # Streamlit auto-routing directory for sidebar pages
    ├── 1_Prices_Metrics.py 
    ├── 2_Fundamentals.py
    └── 3_Correlations.py
```

## Data Sources

* **Market Data:** Live financial data and historical pricing retrieved via the `yfinance` API.
* **On-Chain Data:** Macro fundamental datasets sourced via CSV exports from [DeFiLlama](https://defillama.com/).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/blockchain-analytics.git
   cd blockchain-analytics
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   # On macOS/Linux:
   source .venv/bin/activate  
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Data:**
   Ensure your `Datafiles` folder is populated with the required CSVs from DeFiLlama.

5. **Run the Application:**
   ```bash
   streamlit run home.py
   ```
   The dashboard will automatically open in your default web browser at `http://localhost:8501`.