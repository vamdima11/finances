import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data
AAPL_data = pd.read_csv("../data/AAPL.csv")
AMZN_data = pd.read_csv("../data/AMZN.csv")
BTC_data = pd.read_csv("../data/BTC.csv")
BA_data = pd.read_csv("../data/BA.csv")
GOOGL_data = pd.read_csv("../data/GOOGL.csv")
JNJ_data = pd.read_csv("../data/JNJ.csv")
JPM_data = pd.read_csv("../data/JPM.csv")
MSFT_data = pd.read_csv("../data/MSFT.csv")
NVDA_data = pd.read_csv("../data/NVDA.csv")
TSLA_data = pd.read_csv("../data/TSLA.csv")
V_data = pd.read_csv("../data/V.csv")

data = pd.concat([AAPL_data["close"], AMZN_data["close"], BTC_data["close_price"],
                  BA_data["close"], GOOGL_data["close"], JNJ_data["close"],
                  JPM_data["close"], MSFT_data["close"], NVDA_data["close"],
                  TSLA_data["close"], V_data["close"]], axis=1)
data.columns = ["AAPL", "AMZN", "BTC", "BA", "GOOGL", "JNJ", "JPM", "MSFT", "NVDA", "TSLA", "V"]
data = data.set_index(pd.to_datetime(AAPL_data["date"]))

data.to_csv('../data/general_data.csv')
