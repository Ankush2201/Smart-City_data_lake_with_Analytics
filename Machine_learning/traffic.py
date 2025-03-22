from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.preprocessing import LabelEncoder

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

def train_model():
    data = fetch_data("traffic")
    data = data.dropna()  # Handle missing values

    # Feature Engineering
    X = data[['vehicle_count', 'average_speed']]  # Example features
    y = data['congestion_level']  # Target variable

    # Encode target variable
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Predictions and evaluation
    predictions = model.predict(X_test)
    print(f"Model MSE: {mean_squared_error(y_test, predictions)}")

    # Save model and label encoder
    with open("traffic_model.pkl", "wb") as file:
        pickle.dump(model, file)
    with open("label_encoder.pkl", "wb") as file:
        pickle.dump(label_encoder, file)

train_model()