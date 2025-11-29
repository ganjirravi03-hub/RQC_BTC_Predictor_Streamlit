# utils_api.py
import requests

def fetch_btc_price():
    """
    Alternate endpoint that works on Streamlit Cloud.
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        headers = {"Cache-Control": "no-cache"}

        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        return None

    except:
        return None
        
