from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = FastAPI()
MODEL_PATH = "anomaly_detection_model.pkl"  # Replace with actual model path

# Load model
with open(MODEL_PATH, "rb") as file:
    anomaly_model = pickle.load(file)

# Request body for user input
class AirQualityRequest(BaseModel):
    pm25: float
    pm10: float
    co2: float

# Prediction endpoint
@app.post("/predict")
def get_anomaly_predictions(user_input: AirQualityRequest):
    """
    Detect anomalies in air quality data based on user input.
    Args:
        user_input (AirQualityRequest): JSON object containing 'pm25', 'pm10', and 'co2'.
    Returns:
        A dictionary indicating whether the data is normal or an anomaly.
    """
    # Convert user input to a DataFrame
    input_data = pd.DataFrame([{
        "pm25": user_input.pm25,
        "pm10": user_input.pm10,
        "co2": user_input.co2,
    }])

    # Normalize the input data
    scaler = StandardScaler()
    input_scaled = scaler.fit_transform(input_data)

    # Make anomaly prediction
    anomaly_label = anomaly_model.predict(input_scaled)[0]

    # Return prediction result
    result = "Anomaly" if anomaly_label == -1 else "Normal"
    
    return {"pm25": user_input.pm25,
            "pm10": user_input.pm10,
            "co2": user_input.co2,
            "anomaly_status": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)
