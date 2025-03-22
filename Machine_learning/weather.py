import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import numpy as np
from pymongo import MongoClient

# Flask API base URL
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "smart_city"

# Fetch data from MongoDB
def fetch_data(collection_name):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]
    data = pd.DataFrame(list(collection.find()))
    client.close()
    return data

# Train weather prediction model
def train_weather_model():
    # Fetch weather data from the API
    weather_data = fetch_data("weather")

    # Ensure the data is clean
    weather_data = weather_data.dropna()

    # Feature selection and target variable
    X = weather_data[["humidity", "wind_speed", "rainfall"]]  # Features
    y = weather_data["temperature"]  # Target variable (predicting temperature)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Mean Absolute Error: {mae}")
    print(f"Root Mean Squared Error: {rmse}")

    # Save the trained model for later use
    with open("weather_model.pkl", "wb") as file:
        pickle.dump(model, file)

# Run the model training
train_weather_model()
