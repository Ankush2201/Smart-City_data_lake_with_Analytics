import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px

# Streamlit page configuration
st.set_page_config(page_title="Prediction Dashboard", layout="wide")

# Improved CSS styling
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            font-family: 'Roboto', sans-serif;
        }
        h1, h2, h3, h4, h5 {
            color: #1f4e78;
            font-weight: bold;
        }
        .stMarkdown, .stTextInput, .stButton, .stSelectbox, .stNumberInput {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stButton button {
            background-color: #1f4e78;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #16334d;
        }
        .stSidebar {
            background-color: #f0f4f7;
            padding: 20px;
        }
        .stSidebar h1, .stSidebar h2 {
            color: #1f4e78;
        }
    </style>
""", unsafe_allow_html=True)
# Sidebar: Home Page - Choose Model
st.sidebar.title("Choose Prediction Model")
model_choice = st.sidebar.radio("Select a Model", (
    "Traffic Congestion", 
    "Weather Prediction", 
    "CO2 Level Prediction", 
    "Air Quality Anomaly Detection", 
    "Public Services Prediction"
))

# Traffic Congestion Prediction Page
if model_choice == "Traffic Congestion":
    st.title("Traffic Congestion Prediction")
    st.markdown("### Enter Traffic Data to Predict Congestion Level")

    vehicle_count = st.number_input("Vehicle Count", min_value=0, step=1, value=50)
    average_speed = st.number_input("Average Speed (km/h)", min_value=0.0, step=0.1, value=30.0)

    if st.button("Predict Traffic Congestion"):
        api_url = "http://localhost:8000/predict"
        payload = {"vehicle_count": vehicle_count, "average_speed": average_speed}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()
            congestion_level = prediction['predicted_congestion']
            st.success(f"Predicted Congestion Level: **{congestion_level}**")

            fig = go.Figure(data=[
                go.Bar(name="Vehicle Count", x=["Traffic Data"], y=[vehicle_count], marker_color='#1f78b4'),
                go.Bar(name="Average Speed", x=["Traffic Data"], y=[average_speed], marker_color='#33a02c')
            ])

            fig.update_layout(
                title="Traffic Data vs Prediction",
                xaxis_title="Data Points",
                yaxis_title="Values",
                barmode='group',
                template="plotly_white"
            )

            st.plotly_chart(fig)
            st.write("Prediction Details:")
            st.json(prediction)
        else:
            st.error("Error: Unable to fetch prediction. Please ensure the API is running.")

# Weather Prediction Page
elif model_choice == "Weather Prediction":
    st.title("Weather Prediction")
    st.markdown("### Enter Weather Data to Predict Temperature")

    humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, step=1, value=60)
    wind_speed = st.number_input("Wind Speed (km/h)", min_value=0.0, step=0.1, value=15.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, step=0.1, value=10.0)

    if st.button("Predict Weather Temperature"):
        api_url = "http://localhost:8001/predict"
        payload = {"humidity": humidity, "wind_speed": wind_speed, "rainfall": rainfall}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()
            predicted_temp = prediction['predicted_temperature']
            st.success(f"Predicted Temperature: **{predicted_temp}°C**")

            fig = go.Figure(data=[
                go.Bar(name="Humidity", x=["Weather Data"], y=[humidity], marker_color='#1f78b4'),
                go.Bar(name="Wind Speed", x=["Weather Data"], y=[wind_speed], marker_color='#33a02c'),
                go.Bar(name="Rainfall", x=["Weather Data"], y=[rainfall], marker_color='#ff7f0e')
            ])

            fig.update_layout(
                title="Weather Data vs Prediction",
                xaxis_title="Data Points",
                yaxis_title="Values",
                barmode='group',
                template="plotly_white"
            )

            st.plotly_chart(fig)
            st.write("Prediction Details:")
            st.json(prediction)
        else:
            st.error("Error: Unable to fetch prediction. Please ensure the API is running.")

# CO2 Level Prediction Page
elif model_choice == "CO2 Level Prediction":
    st.title("CO2 Level Prediction")
    st.markdown("### Enter Air Quality Data to Predict CO2 Level")

    pm25 = st.number_input("PM25 (µg/m³)", min_value=0.0, step=0.1, value=30.0)
    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, step=0.1, value=50.0)

    if st.button("Predict CO2 Level"):
        api_url = "http://localhost:8002/predict"
        payload = {"pm25": pm25, "pm10": pm10}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()
            predicted_co2 = prediction['predicted_co2']
            st.success(f"Predicted CO2 Level: **{predicted_co2} µg/m³**")

            fig = px.pie(values=[pm25, pm10], names=["PM25", "PM10"], title="Air Quality Data Distribution")
            st.plotly_chart(fig)
            st.write("Prediction Details:")
            st.json(prediction)
        else:
            st.error("Error: Unable to fetch prediction. Please ensure the API is running.")

# Air Quality Anomaly Detection Page
elif model_choice == "Air Quality Anomaly Detection":
    st.title("Air Quality Anomaly Detection")
    st.markdown("### Enter Air Quality Data to Detect Anomalies")

    pm25 = st.number_input("PM25 (µg/m³)", min_value=0.0, step=0.1, value=30.0)
    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, step=0.1, value=50.0)
    co2 = st.number_input("CO2 (ppm)", min_value=0.0, step=0.1, value=400.0)

    if st.button("Detect Anomaly"):
        api_url = "http://localhost:8003/predict"
        payload = {"pm25": pm25, "pm10": pm10, "co2": co2}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()
            anomaly_status = prediction['anomaly_status']
            st.success(f"Anomaly Detection Result: **{anomaly_status}**")

            fig = go.Figure(data=[
                go.Bar(name="PM25", x=["Air Quality Data"], y=[pm25], marker_color='#1f78b4'),
                go.Bar(name="PM10", x=["Air Quality Data"], y=[pm10], marker_color='#33a02c'),
                go.Bar(name="CO2", x=["Air Quality Data"], y=[co2], marker_color='#ff7f0e')
            ])

            fig.update_layout(
                title="Air Quality Data vs Anomaly Detection",
                xaxis_title="Data Points",
                yaxis_title="Values",
                barmode='group',
                template="plotly_white"
            )

            st.plotly_chart(fig)
            st.write("Prediction Details:")
            st.json(prediction)
        else:
            st.error("Error: Unable to fetch anomaly detection result. Please ensure the API is running.")
elif model_choice == "Public Services Prediction":
    st.title("Public Services Status Prediction")
    st.markdown("### Enter Public Service Data to Predict Operational Status")

    # Dropdown to select service
    service_options = ["Waste Management", "Water", "Electricity"]
    service = st.selectbox("Select Public Service", service_options)

    # Input for service usage
    usage = st.number_input(f"Enter Usage for {service} (units)", min_value=0.0, step=0.1, value=50.0)

    # Button to get prediction
    if st.button("Predict Service Status"):
        # API call to get prediction
        api_url = "http://localhost:8004/predict"
        payload = {"service": service, "usage": usage}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json()
            predicted_status = prediction['predicted_status']
            st.success(f"Predicted Service Status for {service}: **{predicted_status}**")

            # Create bar chart using Plotly
            fig = go.Figure(data=[
                go.Bar(name="Service Usage", x=[f"{service} Data"], y=[usage], marker_color='blue')
            ])

            fig.update_layout(
                title=f"{service} Data vs Prediction",
                xaxis_title="Data Points",
                yaxis_title="Usage (units)",
                barmode='group'
            )

            st.plotly_chart(fig)

            # Show prediction details
            st.write("Prediction Details:")
            st.json(prediction)

            # Add status code mapping
            st.markdown("### Status Code Mapping")
            status_mapping = {
                1: "Operational",
                2: "Partially Operational",
                3: "Non-Operational"
            }
            for code, status in status_mapping.items():
                st.write(f"{code} → {status}")
        else:
            st.error("Error: Unable to fetch prediction. Please ensure the API is running.")