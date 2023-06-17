from predictor_model.models_creator import predict_price

predicted_price = predict_price("BA", "2023-05-02")
print(predicted_price)