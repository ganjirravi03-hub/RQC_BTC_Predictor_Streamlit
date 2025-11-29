# utils_api.py
import requests

def fetch_btc_price():
    """
    Fetch real-time BTC/USDT price from Binance using bookTicker endpoint.
    Returns float price or None if failed.
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
        headers = {"Cache-Control": "no-cache"}

        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["askPrice"])
        return None

    except:
        return None
        
