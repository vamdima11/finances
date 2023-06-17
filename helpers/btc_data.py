import pandas as pd
import requests

# Set API parameters
api_key = "921DEF9E-EC69-44ED-88C3-D5F7AEC9ADFC"

# Set date range
start_date = "2020-01-01T00:00:00"
end_date = "2023-04-14T23:59:59"

# Set asset ID (Bitcoin)
asset_id = "BTC"

# Set symbol ID (USD)
symbol_id = "USD"

# Create empty list to store Bitcoin prices
btc_data = []

# Make API request for Bitcoin prices
url = f'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1DAY&time_start={start_date}'
headers = {'X-CoinAPI-Key': api_key}
response = requests.get(url, headers=headers)
data = response.json()
for item in data:
    btc_data.append({
        "date": item["time_period_start"],
        "open_price": item["price_open"],
        "high_price": item["price_high"],
        "low_price": item["price_low"],
        "close_price": item["price_close"],
        "volume": item["volume_traded"]
    })

# Convert Bitcoin data to a dataframe
btc_df = pd.DataFrame.from_records(btc_data)

# Save data to CSV file
btc_df.to_csv("../data/BTC.csv", index=False)
