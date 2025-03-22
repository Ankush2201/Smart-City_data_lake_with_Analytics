from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

app = FastAPI()
MODEL_PATH = "co2_model.pkl"  # Replace with actual model path

# Load model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Request body for user input
class PredictionRequest(BaseModel):
    pm25: float
    pm10: float

# Prediction endpoint
@app.post("/predict")
def get_predictions(user_input: PredictionRequest):
    """
    Predict CO2 levels based on user input.
    Args:
        user_input (PredictionRequest): JSON object containing 'pm25' and 'pm10'.
    Returns:
        A dictionary with predicted CO2 level.
    """
    # Convert user input to a DataFrame
    input_data = pd.DataFrame([{
        "pm25": user_input.pm25,
        "pm10": user_input.pm10,
    }])

    # Make prediction
    prediction = model.predict(input_data)
    
    return {"pm25": user_input.pm25,
            "pm10": user_input.pm10,
            "predicted_co2": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
