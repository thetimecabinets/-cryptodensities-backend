import json
import requests
from datetime import datetime

def fetch_order_book():
    url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": "BTCUSDT", "limit": 1000}
    response = requests.get(url, params=params)
    data = response.json()

    ticker_url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
    ticker_data = requests.get(ticker_url).json()

    high = float(ticker_data["highPrice"])
    low = float(ticker_data["lowPrice"])
    last = float(ticker_data["lastPrice"])
    volatility = round((high - low) / last * 100, 2)

    result = []

    for side, label in [('bids', 'buy'), ('asks', 'sell')]:
        for price, quantity in data[side]:
            price = float(price)
            quantity = float(quantity)
            value = price * quantity
            if value >= 250000:
                result.append({
                    'exchange': 'Binance',
                    'coin': 'BTC',
                    'type': label,
                    'price': price,
                    'quantity': quantity,
                    'value_usd': round(value),
                    'distance_to_price': f"{abs(price - last) / last * 100:.2f}%",
                    'volatility_1h': volatility,
                    'timestamp': datetime.utcnow().isoformat() + "Z"
                })

    with open("data.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ data.json created")

if __name__ == "__main__":
    fetch_order_book()
