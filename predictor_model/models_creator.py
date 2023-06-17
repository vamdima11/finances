import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the data for each ticker
tickers = ["AAPL", "AMZN", "BTC", "BA", "GOOGL", "JNJ", "JPM", "MSFT", "NVDA", "TSLA", "V"]

data = pd.read_csv('../data/general_data.csv')

# Train the model for each ticker
models = {}
for ticker in tickers:
    # Get the data for the current ticker
    ticker_data = data[[ticker]]
    ticker_data = ticker_data.dropna()

    # Split the data into training and testing sets
    train_data = ticker_data[:-30]
    test_data = ticker_data[-30:]

    # Train the model
    X_train = pd.DataFrame({"days": range(len(train_data.index))})
    y_train = train_data.values.ravel()
    model = RandomForestRegressor().fit(X_train, y_train)

    # Save the model
    models[ticker] = model
    joblib.dump(model, f"../predictor_model/{ticker}.pkl")

# Load the model for a specific ticker and date
def predict_price(ticker, date):
    model = joblib.load(f"../predictor_model/{ticker}.pkl")
    days = (pd.to_datetime(date) - pd.to_datetime(data.index[0])).days
    return model.predict([[days]])[0]