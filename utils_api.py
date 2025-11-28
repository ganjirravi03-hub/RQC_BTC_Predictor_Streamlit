import requests

def fetch_btc_price():
    """
    Fetch real-time BTC/USDT price from Binance API.
    Returns float price if success, otherwise None.
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        else:
            return None

    except Exception:
        return None
        
