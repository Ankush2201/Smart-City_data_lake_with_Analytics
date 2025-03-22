import os
import random
import pandas as pd
import mysql.connector
from flask import Flask, request, jsonify
from faker import Faker
from datetime import datetime
from threading import Thread
import pickle
import time

app = Flask(__name__)
fake = Faker()

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ronit",
    database="olp"
)

cursor = db.cursor()

# Define the function to create tables if they don't exist
def create_metrics_tables():
    # Create table for traffic metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_metrics (
        location VARCHAR(255),
        avg_vehicle_count FLOAT,
        max_speed FLOAT,
        min_speed FLOAT,
        congestion_by_location VARCHAR(255),
        total_vehicle_count FLOAT,
        PRIMARY KEY(location)
    )""")
    
    # Create table for weather metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_metrics (
        location VARCHAR(255),
        avg_temperature FLOAT,
        rainfall_by_location FLOAT,
        humidity_stddev FLOAT,
        temperature_by_location FLOAT,
        max_wind_speed FLOAT,
        PRIMARY KEY(location)
    )""")
    
    # Create table for air quality metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality_metrics (
        location VARCHAR(255),
        max_pm25 FLOAT,
        min_pm10 FLOAT,
        avg_co2 FLOAT,
        total_co2_emission FLOAT,
        PRIMARY KEY(location)
    )""")
    
    # Create table for public services metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public_services_metrics (
        service VARCHAR(255),
        avg_usage FLOAT,
        service_status_distribution VARCHAR(255),
        PRIMARY KEY(service)
    )""")

# Function to insert metrics data into the respective tables
def insert_metrics_into_db(metrics):
    # Insert traffic metrics into the table
    traffic_data = metrics.get("traffic", {})
    for key, value in traffic_data.items():
        cursor.execute("""
        INSERT INTO traffic_metrics (location, avg_vehicle_count, max_speed, min_speed, congestion_by_location, total_vehicle_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        avg_vehicle_count = VALUES(avg_vehicle_count),
        max_speed = VALUES(max_speed),
        min_speed = VALUES(min_speed),
        congestion_by_location = VALUES(congestion_by_location),
        total_vehicle_count = VALUES(total_vehicle_count)
        """, (key, value["avg_vehicle_count"], value["max_speed"], value["min_speed"], value["congestion_by_location"], value["total_vehicle_count"]))
    
    # Insert weather metrics into the table
    weather_data = metrics.get("weather", {})
    for key, value in weather_data.items():
        cursor.execute("""
        INSERT INTO weather_metrics (location, avg_temperature, rainfall_by_location, humidity_stddev, temperature_by_location, max_wind_speed)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        avg_temperature = VALUES(avg_temperature),
        rainfall_by_location = VALUES(rainfall_by_location),
        humidity_stddev = VALUES(humidity_stddev),
        temperature_by_location = VALUES(temperature_by_location),
        max_wind_speed = VALUES(max_wind_speed)
        """, (key, value["avg_temperature"], value["rainfall_by_location"], value["humidity_stddev"], value["temperature_by_location"], value["max_wind_speed"]))
    
    # Insert air quality metrics into the table
    air_quality_data = metrics.get("air_quality", {})
    for key, value in air_quality_data.items():
        cursor.execute("""
        INSERT INTO air_quality_metrics (location, max_pm25, min_pm10, avg_co2, total_co2_emission)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        max_pm25 = VALUES(max_pm25),
        min_pm10 = VALUES(min_pm10),
        avg_co2 = VALUES(avg_co2),
        total_co2_emission = VALUES(total_co2_emission)
        """, (key, value["max_pm25"], value["min_pm10"], value["avg_co2"], value["total_co2_emission"]))
    
    # Insert public services metrics into the table
    public_services_data = metrics.get("public_services", {})
    for key, value in public_services_data.items():
        cursor.execute("""
        INSERT INTO public_services_metrics (service, avg_usage, service_status_distribution)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        avg_usage = VALUES(avg_usage),
        service_status_distribution = VALUES(service_status_distribution)
        """, (key, value["avg_usage"], value["service_status_distribution"]))
    
    # Commit the changes to the database
    db.commit()

# Function to process the metrics pickle file
def process_pickle_and_store():
    # Load the metrics pickle file
    with open("smart_city_metrics.pkl", "rb") as f:
        metrics = pickle.load(f)
    
    # Insert the metrics into the database
    insert_metrics_into_db(metrics)
    
# Start a background thread to process and insert metrics into the database
def start_background_processing():
    # Continuously process and store metrics
    while True:
        process_pickle_and_store()
        time.sleep(60)  # Process and store metrics every 60 seconds

if __name__ == "__main__":
    # Create the necessary tables if they don't exist
    create_metrics_tables()
    
    # Start the background processing in a separate thread
    thread = Thread(target=start_background_processing)
    thread.daemon = True
    thread.start()

    # Run Flask app (for API endpoints)
    app.run(port=5001)
