import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import numpy as np
from pymongo import MongoClient

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

# Train CO2 prediction model
def train_co2_model():
    # Fetch air quality data from the API
    air_quality_data = fetch_data("air_quality")

    # Ensure the data is clean (remove any missing values)
    air_quality_data = air_quality_data.dropna()

    # Feature selection and target variable
    X = air_quality_data[["pm25", "pm10"]]  # Features
    y = air_quality_data["co2"]  # Target variable (predicting CO2 levels)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Regressor model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Mean Absolute Error: {mae}")
    print(f"Root Mean Squared Error: {rmse}")

    # Save the trained model for later use
    with open("co2_model.pkl", "wb") as file:
        pickle.dump(rf_model, file)

# Run the model training
train_co2_model()
