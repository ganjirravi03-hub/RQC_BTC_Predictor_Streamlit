import requests

def fetch_btc_price():
    """
    Fetch real-time BTC/USDT price from Binance (fastest endpoint).
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
        headers = {"Cache-Control": "no-cache"}

        r = requests.get(url, headers=headers, timeout=5)

        if r.status_code == 200:
            data = r.json()
            return float(data["askPrice"])   # most real-time price

        return None

    except:
        return None
        
