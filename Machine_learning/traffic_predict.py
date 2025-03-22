from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

app = FastAPI()
MODEL_PATH = "traffic_model.pkl"
LABEL_ENCODER_PATH = "label_encoder.pkl"

# Load model and label encoder
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open(LABEL_ENCODER_PATH, "rb") as file:
    label_encoder = pickle.load(file)

# Request body for user input
class PredictionRequest(BaseModel):
    vehicle_count: int
    average_speed: float

# Prediction endpoint
@app.post("/predict")
def get_predictions(user_input: PredictionRequest):
    """
    Predict traffic congestion based on user input.
    Args:
        user_input (PredictionRequest): JSON object containing 'vehicle_count' and 'average_speed'.
    Returns:
        A dictionary with predicted congestion.
    """
    # Convert user input to a DataFrame
    input_data = pd.DataFrame([{
        "vehicle_count": user_input.vehicle_count,
        "average_speed": user_input.average_speed,
    }])

    # Make prediction
    prediction = model.predict(input_data)
    congestion_level = label_encoder.inverse_transform(prediction.astype(int))[0]

    return {"vehicle_count": user_input.vehicle_count,
            "average_speed": user_input.average_speed,
            "predicted_congestion": congestion_level}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)