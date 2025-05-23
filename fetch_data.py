
import json
import requests

def fetch_order_data():
    url = "https://api.binance.com/api/v3/depth"
    symbols = ["BTCUSDT", "ETHUSDT"]
    result = {}

    for symbol in symbols:
        params = {"symbol": symbol, "limit": 1000}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            large_bids = [b for b in data["bids"] if float(b[1]) * float(b[0]) >= 250000]
            large_asks = [a for a in data["asks"] if float(a[1]) * float(a[0]) >= 250000]

            result[symbol] = {
                "bids": [{"price": float(b[0]), "amount": float(b[1])} for b in large_bids],
                "asks": [{"price": float(a[0]), "amount": float(a[1])} for a in large_asks],
            }
        except Exception as e:
            result[symbol] = {"error": str(e)}

    with open("data.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    fetch_order_data()
