from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

# Load the trained Random Forest model and label encoders
MODEL_PATH = "public_services_model.pkl"
SERVICE_ENCODER_PATH = "label_encoder_service.pkl"
STATUS_ENCODER_PATH = "label_encoder_status.pkl"

# Load the model and encoders
with open(MODEL_PATH, "rb") as model_file:
    rf_model = pickle.load(model_file)

with open(SERVICE_ENCODER_PATH, "rb") as service_encoder_file:
    service_encoder = pickle.load(service_encoder_file)

with open(STATUS_ENCODER_PATH, "rb") as status_encoder_file:
    status_encoder = pickle.load(status_encoder_file)

# Request body for user input
class PublicServicesRequest(BaseModel):
    service: str
    usage: float

# Prediction endpoint
@app.post("/predict")
def get_service_status_prediction(user_input: PublicServicesRequest):
    """
    Predict the operational status of a service based on user input.
    Args:
        user_input (PublicServicesRequest): JSON object containing 'service' and 'usage'.
    Returns:
        A dictionary with predicted status (Operational, Partially Operational, Non-Operational).
    """
    # Convert user input to a DataFrame
    input_data = pd.DataFrame([{
        "service": user_input.service,
        "usage": user_input.usage,
    }])

    # Encode 'service' into numeric values
    service_encoded = service_encoder.transform(input_data['service'])

    # Prepare the feature set
    input_data['service'] = service_encoded
    X = input_data[['service', 'usage']]

    # Make prediction
    predicted_status_encoded = rf_model.predict(X)[0]
    
    # Decode the predicted status
    predicted_status = status_encoder.inverse_transform([predicted_status_encoded])[0]
    
    return {"service": user_input.service,
            "usage": user_input.usage,
            "predicted_status": predicted_status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8004)
