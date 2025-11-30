import requests

def fetch_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
        headers = {"Cache-Control": "no-cache"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "askPrice" in data and data["askPrice"] is not None:
                return float(data["askPrice"])
            
            print(f"Binance API returned 200 but missing 'askPrice': {data}")
            return None

        print(f"Binance API request failed with status code: {response.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
        
