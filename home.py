import streamlit as st

# Config
st.set_page_config(page_title='Crypto Market & On-Chain Analytics', layout='wide')

# Title
st.title('Crypto Market & On-Chain Analytics')

# Introduction
st.write(
    """
    The digital asset ecosystem spans multiple sectors, from base-layer smart contract platforms to decentralized 
    finance (DeFi) primitives and stablecoin liquidity. This project is designed to track and analyze the market 
    performance and underlying network fundamentals of selected cryptocurrencies.

    Use the **Sidebar** to navigate through different analytical views. Each page addresses a different segment 
    of the crypto industry, allowing you to dive deep into network activity, liquidity flows, and protocol health.
    """
)

st.divider()

# --- Categorized Crypto Logos Section ---
st.header("Tracked Assets by Sector")

# Define categories with coin names and public internet logo URLs
crypto_categories = {
    "Payments & Store of Value": [
        {"name": "Bitcoin (BTC)", "url": "https://cryptologos.cc/logos/bitcoin-btc-logo.png"},
        {"name": "Dogecoin (DOGE)", "url": "https://cryptologos.cc/logos/dogecoin-doge-logo.png"},
        {"name": "Bitcoin Cash (BCH)", "url": "https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png"},
        {"name": "Litecoin (LTC)", "url": "https://cryptologos.cc/logos/litecoin-ltc-logo.png"}
    ],
    "Layer 1 Smart Contract Platforms": [
        {"name": "Ethereum (ETH)", "url": "https://cryptologos.cc/logos/versions/ethereum-eth-logo-colored.svg"},
        {"name": "BNB (BNB)", "url": "https://cryptologos.cc/logos/bnb-bnb-logo.png"},
        {"name": "Solana (SOL)", "url": "https://cryptologos.cc/logos/solana-sol-logo.png"},
        {"name": "TRON (TRX)", "url": "https://cryptologos.cc/logos/tron-trx-logo.png"},
        {"name": "Cardano (ADA)", "url": "https://cryptologos.cc/logos/cardano-ada-logo.png"},
        {"name": "Avalanche (AVAX)", "url": "https://cryptologos.cc/logos/avalanche-avax-logo.png"},
        {"name": "NEAR (NEAR)", "url": "https://cdn.brandfetch.io/id3YSR3bHQ/w/400/h/400/theme/dark/icon.jpeg?c=1dxbfHSJFAPEGdCLU4o5B"},
        {"name": "Hedera (HBAR)", "url": "https://cryptologos.cc/logos/hedera-hbar-logo.png"},
        {"name": "Internet Computer (ICP)", "url": "https://cryptologos.cc/logos/internet-computer-icp-logo.png"}
    ],
    "Stablecoins": [
        {"name": "Tether (USDT)", "url": "https://cryptologos.cc/logos/tether-usdt-logo.png"},
        {"name": "USD Coin (USDC)", "url": "https://cryptologos.cc/logos/usd-coin-usdc-logo.png"},
        {"name": "DAI (DAI)", "url": "https://cryptologos.cc/logos/multi-collateral-dai-dai-logo.png"},
        {"name": "PayPal USD (PYUSD)", "url": "https://s2.coinmarketcap.com/static/img/coins/64x64/27772.png"},
        {"name": "Ethena USDe (USDe)", "url": "https://cryptologos.cc/logos/ethena-usde-usde-logo.png"}
    ],
    "DeFi & Trading Infrastructure": [
        {"name": "Hyperliquid (HYPE)", "url": "Images/Hyperliquid_Blob_Green.png"},
        {"name": "Aerodrome (AERO)", "url": "https://s2.coinmarketcap.com/static/img/coins/64x64/29270.png"}
    ],
    "Data Oracles & Interoperability": [
        {"name": "Chainlink (LINK)", "url": "https://cryptologos.cc/logos/chainlink-link-logo.png"},
        {"name": "Quant (QNT)", "url": "Images/img.png"}
    ],
    "Institutional & Cross-Border": [
        {"name": "XRP (XRP)", "url": "Images/xrp-seeklogo.png"},
        {"name": "Stellar (XLM)", "url": "Images/img_1.png"}
    ],
    "Privacy Networks": [
        {"name": "Monero (XMR)", "url": "https://cryptologos.cc/logos/monero-xmr-logo.png"},
        {"name": "Zcash (ZEC)", "url": "https://cryptologos.cc/logos/zcash-zec-logo.png"}
    ],
    "Layer 2 & Scaling Solutions": [
        {"name": "Polygon (POL)", "url": "https://cryptologos.cc/logos/polygon-matic-logo.png"}
    ],
    "Exchange & Compute Tokens": [
        {"name": "Bitget Token (BGB)", "url": "Images/img_2.png"},
        {"name": "Venice (VVV)", "url": "Images/Venice-Token-VVV-512.png"}
    ]
}
# Brief explanations of each crypto sector
sector_descriptions = {
    "Payments & Store of Value": (
        "Digital assets designed for peer-to-peer payments, transfers, and "
        "potential long-term value preservation. Analyze transaction activity, "
        "liquidity, volatility, and adoption."
    ),
    "Layer 1 Smart Contract Platforms": (
        "Independent blockchain networks that execute transactions and "
        "smart contracts. Compare network activity, transaction fees, "
        "active addresses, developer activity, and ecosystem growth."
    ),
    "Stablecoins": (
        "Tokens designed to maintain a relatively stable value, commonly "
        "pegged to the U.S. dollar. Track supply, market capitalization, "
        "transfer volume, liquidity, and peg stability."
    ),
    "DeFi & Trading Infrastructure": (
        "Protocols that enable decentralized trading, lending, liquidity "
        "provision, and derivatives markets. Examine trading volume, total "
        "value locked (TVL), fees, revenue, and open interest where available."
    ),
    "Data Oracles & Interoperability": (
        "Networks and services that connect blockchains with external data "
        "or enable communication between systems. Evaluate oracle usage, "
        "cross-chain transfers, integrations, and network adoption."
    ),
    "Institutional & Cross-Border": (
        "Assets and networks associated with payment infrastructure, "
        "cross-border transfers, and institutional financial applications. "
        "Study payment activity, settlement metrics, liquidity, and adoption."
    ),
    "Privacy Networks": (
        "Blockchains that provide privacy-focused transaction features. "
        "Analyze available transaction activity, network usage, liquidity, "
        "and adoption while accounting for differences in data visibility."
    ),
    "Layer 2 & Scaling Solutions": (
        "Technologies designed to improve transaction throughput or reduce "
        "costs by processing activity outside a base blockchain or using "
        "other scaling architectures. Compare transaction counts, fees, "
        "active users, and settlement activity."
    ),
    "Exchange & Compute Tokens": (
        "Tokens associated with exchange ecosystems, decentralized trading "
        "platforms, or decentralized computing and AI services. Metrics vary "
        "by project and may include platform usage, fees, token demand, "
        "and compute utilization."
    )
}

# Loop through the dictionary and display logos in a grid format
for category, coins in crypto_categories.items():
    st.markdown(f"### {category}")

    # Display the sector explanation
    st.caption(sector_descriptions.get(category, ""))

    # Create columns (maximum 6 assets per row)
    cols = st.columns(6)

    for i, coin in enumerate(coins):
        col = cols[i % 6]

        with col:
            try:
                st.image(coin["url"], width=50)
                st.caption(coin["name"])
            except Exception:
                st.caption(f"🪙 {coin['name']}")

    st.write("")
