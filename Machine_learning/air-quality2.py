import requests
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
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

# Train anomaly detection model (Isolation Forest)
def train_anomaly_detection_model():
    # Fetch air quality data from the API
    air_quality_data = fetch_data("air_quality")

    # Ensure the data is clean (remove any missing values)
    air_quality_data = air_quality_data.dropna()

    # Feature selection
    X = air_quality_data[["pm25", "pm10", "co2"]]

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest for anomaly detection
    isolation_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    isolation_forest.fit(X_scaled)

    # Predictions: -1 indicates anomaly, 1 indicates normal
    anomaly_labels = isolation_forest.predict(X_scaled)

    # Add anomaly labels to the dataset
    air_quality_data["anomaly"] = anomaly_labels
    print(air_quality_data.head())

    # Count anomalies
    anomalies = air_quality_data[air_quality_data["anomaly"] == -1]
    print(f"Number of anomalies detected: {len(anomalies)}")

    # Save the trained anomaly detection model for later use
    with open("anomaly_detection_model.pkl", "wb") as file:
        pickle.dump(isolation_forest, file)

# Run the model training
train_anomaly_detection_model()
