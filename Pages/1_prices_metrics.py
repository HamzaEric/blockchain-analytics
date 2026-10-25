import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

# Set the page title and header
st.set_page_config(page_title="Crypto Prices Dashboard", layout="wide")
st.title("Cryptocurrency Price")

# Define the categories and their respective symbols
crypto_categories = {
    "Payments & Store of Value": ["BTC-USD", "DOGE-USD", "BCH-USD", "LTC-USD"],
    "Layer 1 Smart Contract Platforms": ["ETH-USD", "BNB-USD", "SOL-USD", "TRX-USD", "ADA-USD", "NEAR-USD", "AVAX-USD",
                                         "ICP-USD", "HBAR-USD"],
    "Stablecoins": ["USDT-USD", "USDC-USD", "USDE-USD", "DAI-USD", "PYUSD-USD"],
    "DeFi & Trading Infrastructure": ["HYPE-USD", "AERO-USD"],
    "Data Oracles & Interoperability": ["LINK-USD", "QNT-USD"],
    "Institutional & Cross-Border": ["XRP-USD", "XLM-USD"],
    "Privacy Networks": ["ZEC-USD", "XMR-USD"],
    "Layer 2 & Scaling Solutions": ["POL-USD"],
    "Centralized Exchange (CEX) Utility": ["BGB-USD"],
    "AI & Decentralized Compute": ["VVV-USD"]
}

# 1. Row for Asset Selection
col1, col2 = st.columns(2)
with col1:
    selected_category = st.selectbox("Select Category", list(crypto_categories.keys()))
with col2:
    selected_symbol = st.selectbox("Select Cryptocurrency", crypto_categories[selected_category])

# 2. Row for Timeframe and Interval Selection
t_col1, t_col2 = st.columns(2)
with t_col1:
    period_options = {
        "Last 1 Month": timedelta(days=30),
        "Last 3 Months": timedelta(days=90),
        "Last 6 Months": timedelta(days=180),
        "Last 1 Year": timedelta(days=365),
        "Last 2 Years": timedelta(days=365 * 2),
        "Last 5 Years": timedelta(days=365 * 5)
    }
    selected_period = st.selectbox("Select Period", list(period_options.keys()))

with t_col2:
    # Add interval selection
    interval_options = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}
    selected_interval = st.selectbox("Select Data Interval", list(interval_options.keys()))
    interval_val = interval_options[selected_interval]

# Date calculations
end_date = datetime.now().date()
start_date = end_date - period_options[selected_period]

date_range = st.slider(
    "Select Date Range",
    value=(start_date, end_date),
    format="YYYY-MM-DD"
)
start_date = date_range[0]
end_date = date_range[1]

# Fetch ticker object and metadata
ticker = yf.Ticker(selected_symbol)
info = ticker.info

# Add Toggle for Moving Averages
show_ma = st.checkbox("Show 50 & 200 Moving Averages")

st.divider()

# Display Live Metrics using ticker.info
metric_cols = st.columns(4)
latest_data = ticker.history(period="1d")

if not latest_data.empty:
    current_price = latest_data["Close"].iloc[-1]

    # Safely extract info dict values
    market_cap = info.get("marketCap", "N/A")
    vol_24h = info.get("volume24Hr", "N/A")
    circ_supply = info.get("circulatingSupply", "N/A")


    # Format large numbers
    def format_large_num(num):
        if num == "N/A" or num is None: return "N/A"
        if num >= 1e9: return f"${num / 1e9:.2f}B"
        if num >= 1e6: return f"${num / 1e6:.2f}M"
        return f"${num:,.0f}"


    metric_cols[0].metric(label=f"Latest Price", value=f"${current_price:,.4f}")
    metric_cols[1].metric(label="Market Cap", value=format_large_num(market_cap))
    metric_cols[2].metric(label="24h Volume", value=format_large_num(vol_24h))

    if circ_supply != "N/A" and circ_supply is not None:
        metric_cols[3].metric(label="Circulating Supply", value=f"{circ_supply:,.0f}")
    else:
        metric_cols[3].metric(label="Circulating Supply", value="N/A")

    # Fetch the historical price data
    crypto_data = yf.download(selected_symbol, start=start_date, end=end_date, interval=interval_val)

    if not crypto_data.empty:
        # Flatten the MultiIndex columns returned by newer versions of yfinance
        if isinstance(crypto_data.columns, pd.MultiIndex):
            crypto_data.columns = crypto_data.columns.get_level_values(0)

        # Calculate Moving Averages
        if show_ma:
            crypto_data['SMA_50'] = crypto_data['Close'].rolling(window=50).mean()
            crypto_data['SMA_200'] = crypto_data['Close'].rolling(window=200).mean()

        # Create a single figure
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Create a secondary y-axis for Volume
        ax2 = ax1.twinx()

        # Plot Volume first on the secondary axis (attractive soft purple color)
        ax2.bar(crypto_data.index, crypto_data["Volume"], color="#9b59b6", alpha=0.25, width=0.8, label="Volume")

        # Scale the secondary y-axis so the volume bars only occupy the bottom ~30% of the chart
        max_vol = crypto_data["Volume"].max()
        ax2.set_ylim(0, max_vol * 3.5)
        ax2.set_ylabel("Volume", color="#9b59b6", alpha=0.8)
        ax2.tick_params(axis='y', labelcolor="#9b59b6")

        # Plot Price & MAs on the primary axis
        ax1.plot(crypto_data.index, crypto_data["Close"], label="Close Price", color="#29b5e8", linewidth=2)

        if show_ma:
            ax1.plot(crypto_data.index, crypto_data['SMA_50'], label="50-Period SMA", color="orange", linewidth=1.5,
                     alpha=0.9)
            ax1.plot(crypto_data.index, crypto_data['SMA_200'], label="200-Period SMA", color="red", linewidth=1.5,
                     alpha=0.9)

        ax1.set_ylabel("Closing Price (USD)")
        ax1.set_title(f"{selected_symbol} Price & Volume ({start_date} to {end_date})", loc="left")

        # Combine legends from both axes
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", frameon=False)

        # Ensure the price line renders on top of the volume bars
        ax1.set_zorder(ax2.get_zorder() + 1)
        ax1.patch.set_visible(False)

        # Formatting
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.grid(alpha=0.2)

        st.pyplot(fig)

        # Display data in a table
        with st.expander("View Raw Historical Data"):
            st.dataframe(crypto_data, use_container_width=True)
    else:
        st.warning(f"Failed to fetch historical {selected_symbol} price data for the selected range/interval.")
else:
    st.warning(f"Failed to fetch latest {selected_symbol} price data.")