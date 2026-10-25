import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Page Config
st.set_page_config(page_title="Network Fundamentals", page_icon="📊", layout="wide")
st.title("On-Chain Network Fundamentals")
st.write("Comprehensive analysis of Total Value Locked (TVL), DEX Volumes, and Stablecoin liquidity.")


# Helper function to format large numbers
def format_large_num(num):
    if pd.isna(num): return "N/A"
    if num >= 1e9: return f"${num / 1e9:.2f}B"
    if num >= 1e6: return f"${num / 1e6:.2f}M"
    if num >= 1e3: return f"${num / 1e3:.2f}K"
    return f"${num:,.2f}"


# Helper function to parse Stablecoin JSON supply
def parse_circulating(val):
    try:
        d = json.loads(val)
        return list(d.values())[0]
    except:
        return 0.0


# Define potential paths for the data files
data_dir = "Datafiles" if os.path.exists("Datafiles") else "."


# Load datasets safely
@st.cache_data
def load_data():
    data = {}
    files = {
        "chains_tvl": "chains TVL.csv",
        "dex_vol": "dex-volumes.csv",
        "stables": "stablecoins.csv",
        "stables_chains": "stablecoins-chains.csv"
    }

    for key, filename in files.items():
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            data[key] = pd.read_csv(path)
        else:
            data[key] = pd.DataFrame()  # Empty dataframe if not found

    # Pre-process stablecoins JSON column if data exists
    if not data["stables"].empty and "circulating" in data["stables"].columns:
        data["stables"]["circulating_usd"] = data["stables"]["circulating"].apply(parse_circulating)

    return data


data = load_data()

# Check if data loaded successfully
if all(df.empty for df in data.values()):
    st.error(
        "Could not find the required CSV files. Please ensure they are in the current directory or a 'Datafiles' folder.")
    st.stop()

# Create Tabs for the 4 distinct datasets
tab1, tab2, tab3, tab4 = st.tabs([
    " Chains TVL",
    " DEX Volumes",
    " Stablecoins Overview",
    " Stablecoins by Chain"
])

# ==========================================
# TAB 1: CHAINS TVL
# ==========================================
with tab1:
    df_tvl = data.get("chains_tvl")
    if not df_tvl.empty:
        st.subheader("Base Layer Total Value Locked (TVL)")

        # Top-level metrics
        total_global_tvl = df_tvl['tvl'].sum()
        top_chain = df_tvl.loc[df_tvl['tvl'].idxmax()]

        col1, col2 = st.columns(2)
        col1.metric("Global TVL Across All Chains", format_large_num(total_global_tvl))
        col2.metric("Dominant Chain", top_chain['name'], format_large_num(top_chain['tvl']))

        st.divider()

        # Interactive Controls
        top_n_chains = st.slider("Select number of top chains to view", min_value=5, max_value=50, value=15,
                                 key="tvl_slider")

        plot_data = df_tvl.sort_values(by="tvl", ascending=False).head(top_n_chains)

        # Chart
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(plot_data['name'], plot_data['tvl'], color="#3498db", edgecolor="black", linewidth=0.5)

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_large_num(x)))
        ax.set_ylabel("Total Value Locked (USD)")
        ax.set_title(f"Top {top_n_chains} Chains by TVL", loc="left", fontweight="bold")
        plt.xticks(rotation=45, ha='right')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.2)

        st.pyplot(fig)

        with st.expander("View Full TVL Dataset"):
            st.dataframe(df_tvl.sort_values(by='tvl', ascending=False), use_container_width=True)
    else:
        st.warning("chains TVL.csv not found.")

# ==========================================
# TAB 2: DEX VOLUMES
# ==========================================
with tab2:
    df_dex = data.get("dex_vol")
    if not df_dex.empty:
        st.subheader("Decentralized Exchange (DEX) Activity")

        col1, col2 = st.columns([1, 3])
        with col1:
            # Volume Metric Selector
            vol_metrics = {
                "24H Volume": "total24h",
                "7D Volume": "total7d",
                "30D Volume": "total30d",
                "All Time Volume": "totalAllTime"
            }
            selected_vol_label = st.radio("Select Volume Timeframe", list(vol_metrics.keys()))
            selected_vol_col = vol_metrics[selected_vol_label]
            top_n_dex = st.slider("Top DEXes to display", 5, 30, 15, key="dex_slider")

        with col2:
            # Clean NaN values for the selected metric
            plot_data_dex = df_dex.dropna(subset=[selected_vol_col]).sort_values(by=selected_vol_col,
                                                                                 ascending=False).head(top_n_dex)

            fig2, ax2 = plt.subplots(figsize=(12, 6))
            ax2.bar(plot_data_dex['name'], plot_data_dex[selected_vol_col], color="#9b59b6")

            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_large_num(x)))
            ax2.set_ylabel(f"Volume (USD)")
            ax2.set_title(f"Top {top_n_dex} DEXes by {selected_vol_label}", loc="left", fontweight="bold")
            plt.xticks(rotation=45, ha='right')

            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.grid(axis='y', alpha=0.2)

            st.pyplot(fig2)

        st.divider()
        st.markdown("**DEX Performance & Growth Metrics**")
        # Display growth columns clearly
        display_cols = ['name', 'category', 'chains', 'total24h', 'total30d', 'change_1d', 'change_7d', 'change_1m']
        st.dataframe(df_dex[display_cols].sort_values(by='total24h', ascending=False).head(50),
                     use_container_width=True)
    else:
        st.warning("dex-volumes.csv not found.")

# ==========================================
# TAB 3: STABLECOINS OVERVIEW
# ==========================================
with tab3:
    df_stables = data.get("stables")
    if not df_stables.empty:
        st.subheader("Global Stablecoin Market")

        total_stables_supply = df_stables['circulating_usd'].sum()

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Global Stablecoin Supply", format_large_num(total_stables_supply))
        m2.metric("Number of Tracked Stablecoins", len(df_stables[df_stables['circulating_usd'] > 0]))

        # Calculate dominance of the top stablecoin
        top_stable = df_stables.loc[df_stables['circulating_usd'].idxmax()]
        dominance = (top_stable['circulating_usd'] / total_stables_supply) * 100
        m3.metric(f"{top_stable['symbol']} Market Dominance", f"{dominance:.2f}%")

        st.divider()

        top_n_stables = st.slider("Select top stablecoins to view", 5, 20, 10, key="stables_slider")
        plot_data_stables = df_stables.sort_values(by='circulating_usd', ascending=False).head(top_n_stables)

        fig3, ax3 = plt.subplots(figsize=(12, 5))
        bars = ax3.barh(plot_data_stables['symbol'][::-1], plot_data_stables['circulating_usd'][::-1], color="#27ae60")

        ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_large_num(x)))
        ax3.set_xlabel("Circulating Supply (USD)")
        ax3.set_title(f"Top {top_n_stables} Stablecoins by Circulating Supply", loc="left", fontweight="bold")

        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='x', alpha=0.2)

        st.pyplot(fig3)

        with st.expander("View Full Stablecoin Data & Peg Mechanics"):
            st.dataframe(df_stables[['name', 'symbol', 'pegType', 'pegMechanism', 'circulating_usd', 'price',
                                     'chains']].sort_values(by='circulating_usd', ascending=False),
                         use_container_width=True)
    else:
        st.warning("stablecoins.csv not found.")

# ==========================================
# TAB 4: STABLECOINS BY CHAIN
# ==========================================
with tab4:
    df_stables_chains = data.get("stables_chains")
    if not df_stables_chains.empty:
        st.subheader("Stablecoin Liquidity Distribution by Blockchain")

        top_n_stables_chains = st.slider("Top chains to display", 5, 30, 15, key="stables_chains_slider")
        plot_data_sc = df_stables_chains.sort_values(by='totalCirculatingUSD', ascending=False).head(
            top_n_stables_chains)

        fig4, ax4 = plt.subplots(figsize=(12, 6))
        ax4.bar(plot_data_sc['name'], plot_data_sc['totalCirculatingUSD'], color="#e67e22")

        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_large_num(x)))
        ax4.set_ylabel("Total Circulating Stablecoins (USD)")
        ax4.set_title(f"Top {top_n_stables_chains} Chains by Stablecoin Supply", loc="left", fontweight="bold")
        plt.xticks(rotation=45, ha='right')

        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.grid(axis='y', alpha=0.2)

        st.pyplot(fig4)

        with st.expander("View Full Distribution Dataset"):
            st.dataframe(df_stables_chains.sort_values(by='totalCirculatingUSD', ascending=False),
                         use_container_width=True)
    else:
        st.warning("stablecoins-chains.csv not found.")