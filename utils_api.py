import requests
import streamlit as st

# ========== COINBASE ==========
@st.cache_data(ttl=10)
def get_price_coinbase():
    try:
        response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5)
        data = response.json()
        return float(data["data"]["amount"])
    except:
        return None


# ========== KRAKEN ==========
@st.cache_data(ttl=10)
def get_price_kraken():
    try:
        response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD", timeout=5)
        data = response.json()
        return float(data["result"]["XXBTZUSD"]["c"][0])
    except:
        return None


# ========== COINGECKO ==========
@st.cache_data(ttl=10)
def get_price_coingecko():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=5
        )
        data = response.json()
        return float(data["bitcoin"]["usd"])
    except:
        return None


# MAIN FUNCTION TO GET LIVE AVG PRICE
def get_live_btc_price():
    prices = []

    coinbase = get_price_coinbase()
    if coinbase: prices.append(coinbase)

    kraken = get_price_kraken()
    if kraken: prices.append(kraken)

    coingecko = get_price_coingecko()
    if coingecko: prices.append(coingecko)

    if len(prices) == 0:
        return None

    return sum(prices) / len(prices)
    
