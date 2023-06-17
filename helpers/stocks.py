import requests
import pandas as pd
import matplotlib.pyplot as plt

# Запрос данных акций
stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "BA", "TSLA", "NVDA", "JPM", "JNJ", "V"]
start_date = "2020-01-01"
end_date = "2023-04-14"

params = {
  'access_key': 'eaa71144b70e7100ab9e33401f183fc3'
}

# stock_data = []
# for stock in stocks:
#     url = f"http://api.marketstack.com/v1/eod?" \
#           f"access_key={params['access_key']}&" \
#           f"symbols={stock}" \
#           f"&date_from={start_date}" \
#           f"&date_to={end_date}"
#     response = requests.get(url, params)
#     data = response.json()
#
#     stock_df = pd.DataFrame.from_records(data["data"])
#     stock_df["symbol"] = stock
#     stock_df.to_csv(f"../data/{stock}.csv", index=False)

# Запрос данных курса валют
# currency_data = {}
# currencies = ["USD", "EUR"]
# for currency in currencies:
#     url = f"http://api.marketstack.com/v1/eod?" \
#           f"access_key={params['access_key']}&" \
#           f"symbols={currency}" \
#           f"&date_from={start_date}" \
#           f"&date_to={end_date}"
#     response = requests.get(url)
#     data = response.json()
#     currency_df = pd.DataFrame.from_records(data["data"])
#     currency_df.to_csv(f"../data/{currency}.csv", index=False)


# Set API parameters
headers = {"x-access-token": "goldapi-bwjhhurlggl6pv7-io"}

# Create empty lists to store gold and silver data
gold_data = []
silver_data = []

# Iterate over each day in the date range
date = pd.to_datetime(start_date)
while date <= pd.to_datetime(end_date):
    date_str = date.strftime("%Y-%m-%d")
    print(date_str)

    # Request gold prices for the current day
    gold_url = f"https://www.goldapi.io/api/XAU/USD/{date_str}"
    gold_response = requests.get(gold_url, headers=headers)
    gold_json = gold_response.json()
    gold_data.append({"date": date_str, "gold_price": gold_json["price"]})

    # Request silver prices for the current day
    silver_url = f"https://www.goldapi.io/api/XAG/USD/{date_str}"
    silver_response = requests.get(silver_url, headers=headers)
    silver_json = silver_response.json()
    silver_data.append({"date": date_str, "silver_price": silver_json["price"]})

    # Increment date by one day
    date += pd.Timedelta(days=1)

# Convert gold and silver data to dataframes
gold_df = pd.DataFrame.from_records(gold_data)
silver_df = pd.DataFrame.from_records(silver_data)

# Merge gold and silver data into a single dataframe
df = pd.merge(gold_df, silver_df, on="date", how="outer")

# Save data to CSV file
df.to_csv("../data/gold_silver_prices.csv", index=False)
