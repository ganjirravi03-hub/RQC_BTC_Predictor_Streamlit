import requests

# ⛽ Universal API Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -------------------------------
#  A) Coinbase API (BTC-USD)
# -------------------------------
def get_price_coinbase():
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()
        return float(data["data"]["amount"])
    except:
        return None

# -------------------------------
#  B) Kraken API (BTCUSD)
# -------------------------------
def get_price_kraken():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD"
        r = requests.get(url, headers=HEADERS, timeout=5)
        data = r.json()
        price = float(data["result"]["XBTUSD"]["c"][0])
        return price
    except:
        return None

# -------------------------------
#  C) CoinGecko API (BTC)
# -------------------------------
def get_price_coingecko():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, headers=HEADERS, timeout=5)
        return float(r.json()["bitcoin"]["usd"])
    except:
        return None

# -------------------------------
#  INR Conversion (USD → INR)
# -------------------------------
def get_inr_rate():
    try:
        url = "https://api.exchangerate.host/latest?base=USD&symbols=INR"
        r = requests.get(url, timeout=5)
        return float(r.json()["rates"]["INR"])
    except:
        return 83.10  # fallback INR rate

# -------------------------------
#  FINAL Price Fetcher (Auto Fallback)
# -------------------------------
def get_live_btc_price():
    price = (
        get_price_coinbase()
        or get_price_kraken()
        or get_price_coingecko()
    )
    return price

