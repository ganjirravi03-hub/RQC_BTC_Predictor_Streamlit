import requests

def fetch_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "BTCUSDT"}

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        return float(data["price"])
    except Exception as e:
        print("API Error:", e)
        return None
        
