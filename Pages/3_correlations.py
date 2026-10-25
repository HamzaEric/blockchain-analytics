import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="Quantitative Correlations", page_icon="📈", layout="wide")
st.title("Price vs. Fundamentals Correlation")
st.write("""
Overlay historical price action against fundamental on-chain time-series data. 
This dashboard automatically loads Solana's on-chain data to correlate with its market price.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Market Data")
    # Defaulting to SOL-USD
    ticker_symbol = st.text_input("Ticker Symbol", value="SOL-USD")
    years = st.slider("Years of Price History", 1, 5, 2)

with col2:
    st.subheader("2. On-Chain Data")

    # Hardcoding the path to automatically load solana.csv
    file_path = os.path.join("Datafiles", "solana.csv")

    if os.path.exists(file_path):
        st.success("✅ Automatically loaded: `solana.csv`")
        data_loaded = True
    else:
        st.error("❌ `solana.csv` not found. Please ensure it is inside the 'Datafiles' folder.")
        data_loaded = False

st.divider()

if data_loaded and ticker_symbol:
    # --- Process On-Chain Data ---
    df_fund = pd.read_csv(file_path)

    # Try to find a date column
    date_col = next((col for col in df_fund.columns if 'date' in col.lower() or 'time' in col.lower()), None)

    if not date_col:
        st.error("Could not detect a Date column in solana.csv.")
        st.stop()

    # --- SMART DATETIME PARSING ---
    if pd.api.types.is_numeric_dtype(df_fund[date_col]):
        # If the number is huge, it's in milliseconds. Otherwise, it's in seconds.
        if df_fund[date_col].max() > 1e11:
            df_fund[date_col] = pd.to_datetime(df_fund[date_col], unit='ms')
        else:
            df_fund[date_col] = pd.to_datetime(df_fund[date_col], unit='s')
    else:
        # If it's a string like "2023-10-05"
        df_fund[date_col] = pd.to_datetime(df_fund[date_col])

    # Normalize to date only for merging
    df_fund[date_col] = df_fund[date_col].dt.date
    df_fund.set_index(date_col, inplace=True)

    # Select the metric column (assuming it's the first numeric column that isn't the date)
    numeric_cols = df_fund.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        st.error("No numeric metrics found in the CSV.")
        st.stop()

    metric_col = st.selectbox("Select Fundamental Metric to Correlate", numeric_cols)

    # --- Process Price Data ---
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365 * years)

    ticker = yf.Ticker(ticker_symbol)
    df_price = ticker.history(start=start_date, end=end_date)

    if df_price.empty:
        st.error(f"Could not fetch price data for {ticker_symbol}.")
        st.stop()

    # Flatten MultiIndex columns returned by newer versions of yfinance
    if isinstance(df_price.columns, pd.MultiIndex):
        df_price.columns = df_price.columns.get_level_values(0)

    df_price.index = df_price.index.date

    # --- Merge Datasets ---
    # Inner join on the date index so we only compare days where we have both price and fundamentals
    merged_df = df_price[['Close']].join(df_fund[[metric_col]], how='inner')
    merged_df.dropna(inplace=True)

    if merged_df.empty:
        st.warning("No overlapping dates found between the price data and the fundamental data.")
    else:
        # Calculate Pearson Correlation
        correlation = merged_df['Close'].corr(merged_df[metric_col])

        # Display Metrics
        st.subheader("Correlation Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Data Points Analyzed", len(merged_df))
        m2.metric(f"Pearson Correlation (R)", f"{correlation:.3f}",
                  help="1.0 is a perfect positive correlation, -1.0 is a perfect negative correlation.")

        # Interpret correlation
        if correlation > 0.7:
            interpretation = "Strong Positive (Fundamentals drive price)"
        elif correlation < -0.7:
            interpretation = "Strong Negative (Inverse relationship)"
        elif correlation > 0.3:
            interpretation = "Weak Positive"
        elif correlation < -0.3:
            interpretation = "Weak Negative"
        else:
            interpretation = "No Meaningful Correlation"

        m3.metric("Interpretation", interpretation)

        # --- Dual Axis Chart ---
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot Price on primary Y axis
        color1 = '#29b5e8'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price (USD)', color=color1, fontweight='bold')
        line1 = ax1.plot(merged_df.index, merged_df['Close'], color=color1, label=f"{ticker_symbol} Price", linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color1)

        # Plot Fundamental Metric on secondary Y axis
        ax2 = ax1.twinx()
        color2 = '#e74c3c'
        ax2.set_ylabel(metric_col, color=color2, fontweight='bold')
        line2 = ax2.plot(merged_df.index, merged_df[metric_col], color=color2, label=metric_col, linewidth=2, alpha=0.8)
        ax2.tick_params(axis='y', labelcolor=color2)

        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', frameon=False)

        ax1.set_title(f"{ticker_symbol} Price vs. {metric_col}", loc='left')
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.grid(alpha=0.2)

        st.pyplot(fig)

        with st.expander("View Merged Dataset"):
            st.dataframe(merged_df, use_container_width=True)