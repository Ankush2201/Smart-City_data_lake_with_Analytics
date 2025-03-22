import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from sklearn.preprocessing import LabelEncoder
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

# Train model using the data fetched from the Flask API
def train_model():
    # Fetch public services data from the API
    data = fetch_data("public_services")
    
    # Ensure the data is clean
    data = data.dropna()

    # Feature engineering:
    # Encode 'service' column (categorical) into numeric values using LabelEncoder
    label_encoder_service = LabelEncoder()
    data['service'] = label_encoder_service.fit_transform(data['service'])

    # Select features ('service' and 'usage') and target ('status')
    X = data[['service', 'usage']]  # Features: 'service' (encoded) and 'usage'
    y = data['status']  # Target: 'status' (Operational, Partially Operational, Non-Operational)

    # Encode the target variable (status)
    label_encoder_status = LabelEncoder()
    y = label_encoder_status.fit_transform(y)  # Encode status to numerical values

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Save the model and label encoders for later use
    with open("public_services_model.pkl", "wb") as file:
        pickle.dump(model, file)
    with open("label_encoder_service.pkl", "wb") as file:
        pickle.dump(label_encoder_service, file)
    with open("label_encoder_status.pkl", "wb") as file:
        pickle.dump(label_encoder_status, file)

# Run the model training
train_model()
