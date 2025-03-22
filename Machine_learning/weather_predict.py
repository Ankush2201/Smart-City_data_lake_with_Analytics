from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np

app = FastAPI()

# Paths for the trained model and label encoder (if needed)
MODEL_PATH = "weather_model.pkl"

# Load the trained weather prediction model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Request body for user input (humidity, wind speed, rainfall)
class WeatherPredictionRequest(BaseModel):
    humidity: int
    wind_speed: float
    rainfall: float

# Prediction endpoint
@app.post("/predict")
def get_weather_predictions(user_input: WeatherPredictionRequest):
    """
    Predict temperature based on user input for weather data.
    Args:
        user_input (WeatherPredictionRequest): JSON object containing 'humidity', 'wind_speed', and 'rainfall'.
    Returns:
        A dictionary with predicted temperature.
    """
    # Convert user input to a DataFrame
    input_data = pd.DataFrame([{
        "humidity": user_input.humidity,
        "wind_speed": user_input.wind_speed,
        "rainfall": user_input.rainfall,
    }])

    # Make prediction
    prediction = model.predict(input_data)

    return {"humidity": user_input.humidity,
            "wind_speed": user_input.wind_speed,
            "rainfall": user_input.rainfall,
            "predicted_temperature": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
