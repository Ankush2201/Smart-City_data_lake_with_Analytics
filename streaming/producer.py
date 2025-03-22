import logging
import signal
import sys
import requests
import json
import time
import random
from confluent_kafka import Producer

# Kafka configuration
BROKER = 'localhost:9094'
TOPICS = {
    "traffic": "traffic_topic",
    "weather": "weather_topic",
    "air_quality": "air_quality_topic",
    "public_services": "public_services_topic"
}

# Confluent Kafka producer configuration
producer_config = {
    'bootstrap.servers': BROKER,
    'client.id': 'smart-city-producer',
    'retries': 5  # Enable retries for better reliability
}

# Initialize Kafka producer
producer = Producer(producer_config)

# API URLs
API_BASE_URL = "http://127.0.0.1:5000"
ENDPOINTS = {
    "traffic": f"{API_BASE_URL}/traffic",
    "weather": f"{API_BASE_URL}/weather",
    "air_quality": f"{API_BASE_URL}/air-quality",
    "public_services": f"{API_BASE_URL}/public-services"
}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Graceful shutdown handler
def signal_handler(sig, frame):
    logger.info('Shutting down gracefully...')
    producer.flush()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Callback function for delivery report
def delivery_report(err, msg):
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [partition: {msg.partition()}]")

def fetch_and_send_data():
    while True:
        for data_type, endpoint in ENDPOINTS.items():
            try:
                response = requests.get(endpoint)
                if response.status_code == 200:
                    data = response.json()
                    for record in data:
                        producer.produce(
                            topic=TOPICS[data_type],
                            value=json.dumps(record),
                            key=record.get("location", "default_key"),
                            callback=delivery_report
                        )
                        producer.poll(0)  # Trigger delivery report
                    logger.info(f"Published {len(data)} records to '{TOPICS[data_type]}'")
                else:
                    logger.error(f"Failed to fetch data from {endpoint}: {response.status_code}")
            except Exception as e:
                logger.error(f"Error in producing data for {data_type}: {e}")

        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    logger.info("Starting producer.")
    fetch_and_send_data()
