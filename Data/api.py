from flask import Flask, jsonify, request
from faker import Faker
import random
import threading
import time
import csv
import os
from datetime import datetime

app = Flask(__name__)
fake = Faker()

# File names for each data type
TRAFFIC_FILE = "traffic_data.csv"
WEATHER_FILE = "weather_data.csv"
AIR_QUALITY_FILE = "air_quality_data.csv"
PUBLIC_SERVICES_FILE = "public_services_data.csv"

# Control flags for operations
continue_generating = True

# List of sections in Mumbai
mumbai_sections = [
    "Andheri", "Bandra", "Borivali", "Colaba", "Dadar", "Ghatkopar", "Jogeshwari", 
    "Kandivali", "Kurla", "Malad", "Marine Drive", "Mulund", "Nariman Point", 
    "Parel", "Prabhadevi", "Saki Naka", "Santacruz", "Sion", "Vashi", "Worli", 
    "Versova", "Chembur", "Vile Parle", "Lower Parel", "Matunga", "Mahalaxmi", 
    "Khar", "Dahisar", "Thane", "Kandivali East", "Kandivali West", "Bhayandar"
]

# Function to initialize CSV files
def initialize_csv(file_name, headers):
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

# Initialize all CSV files with appropriate headers
initialize_csv(TRAFFIC_FILE, ["location", "vehicle_count", "average_speed", "congestion_level", "timestamp"])
initialize_csv(WEATHER_FILE, ["location", "temperature", "humidity", "rainfall", "wind_speed", "timestamp"])
initialize_csv(AIR_QUALITY_FILE, ["location", "pm25", "pm10", "co2", "timestamp"])
initialize_csv(PUBLIC_SERVICES_FILE, ["service", "usage", "status", "timestamp"])

# Functions to generate synthetic data for each type
def generate_traffic_data():
    location = random.choice(mumbai_sections)  # Random section from Mumbai
    vehicle_count = random.randint(50, 1000)
    average_speed = round(random.uniform(20, 100), 2)
    congestion_level = random.choice(["Low", "Moderate", "High"])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [location, vehicle_count, average_speed, congestion_level, timestamp]

def generate_weather_data():
    location = random.choice(mumbai_sections)  # Random section from Mumbai
    temperature = round(random.uniform(-10, 40), 2)
    humidity = random.randint(20, 100)
    rainfall = round(random.uniform(0, 200), 2)  # mm
    wind_speed = round(random.uniform(0, 20), 2)  # km/h
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [location, temperature, humidity, rainfall, wind_speed, timestamp]

def generate_air_quality_data():
    location = random.choice(mumbai_sections)  # Random section from Mumbai
    pm25 = round(random.uniform(0, 500), 2)
    pm10 = round(random.uniform(0, 500), 2)
    co2 = round(random.uniform(300, 5000), 2)  # ppm
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [location, pm25, pm10, co2, timestamp]

def generate_public_services_data():
    service = random.choice(["Water", "Electricity", "Waste Management"])
    usage = round(random.uniform(100, 10000), 2)  # liters/kWh/tons
    status = random.choice(["Operational", "Partially Operational", "Non-Operational"])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return [service, usage, status, timestamp]

# Background thread to continuously generate data
def generate_data_continuously():
    global continue_generating
    while continue_generating:
        with open(TRAFFIC_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(generate_traffic_data())

        with open(WEATHER_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(generate_weather_data())

        with open(AIR_QUALITY_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(generate_air_quality_data())

        with open(PUBLIC_SERVICES_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(generate_public_services_data())

        # Wait for 5 seconds
        time.sleep(5)

# API endpoints to fetch recent data
@app.route('/traffic', methods=['GET'])
def get_traffic_data():
    data = []
    with open(TRAFFIC_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)[-10:]  # Return the last 10 entries
    return jsonify(data)

@app.route('/weather', methods=['GET'])
def get_weather_data():
    data = []
    with open(WEATHER_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)[-10:]
    return jsonify(data)

@app.route('/air-quality', methods=['GET'])
def get_air_quality_data():
    data = []
    with open(AIR_QUALITY_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)[-10:]
    return jsonify(data)

@app.route('/public-services', methods=['GET'])
def get_public_services_data():
    data = []
    with open(PUBLIC_SERVICES_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)[-10:]
    return jsonify(data)

# API endpoint to fetch all data from a specific category
@app.route('/fetch-all/<data_type>', methods=['GET'])
def fetch_all_data(data_type):
    file_mapping = {
        "traffic": TRAFFIC_FILE,
        "weather": WEATHER_FILE,
        "air-quality": AIR_QUALITY_FILE,
        "public-services": PUBLIC_SERVICES_FILE
    }
    file_name = file_mapping.get(data_type)
    if not file_name or not os.path.exists(file_name):
        return jsonify({"error": "Invalid data type or no data available."}), 404

    data = []
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return jsonify(data)

# API endpoint to stop or start data generation
@app.route('/control-generation', methods=['POST'])
def control_generation():
    global continue_generating
    action = request.json.get("action")
    if action == "stop":
        continue_generating = False
        return jsonify({"message": "Data generation stopped."})
    elif action == "start":
        if not continue_generating:
            continue_generating = True
            threading.Thread(target=generate_data_continuously, daemon=True).start()
        return jsonify({"message": "Data generation started."})
    else:
        return jsonify({"error": "Invalid action. Use 'start' or 'stop'."}), 400

if __name__ == '__main__':
    # Start the background thread for data generation
    threading.Thread(target=generate_data_continuously, daemon=True).start()
    app.run(port=5000)
