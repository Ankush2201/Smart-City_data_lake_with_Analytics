
---

# Smart City Data Lake with Analytics

## Table of Contents
- [Overview](#overview)
- [Project Architecture](#project-architecture)
- [Modules and File Descriptions](#modules-and-file-descriptions)
  - [Root Configuration Files](#root-configuration-files)
  - [Data Sources](#data-sources)
  - [Data Lake](#data-lake)
  - [Streaming Infrastructure](#streaming-infrastructure)
  - [Machine Learning Components](#machine-learning-components)
  - [Dashboard](#dashboard)
- [Theoretical Background](#theoretical-background)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Deployment with Docker](#deployment-with-docker)
- [Testing and Future Improvements](#testing-and-future-improvements)
- [License](#license)

---

## Overview

The **Smart City Data Lake with Analytics** project is a comprehensive simulation of a smart city analytics ecosystem. It is designed to:

- **Ingest Data:** Collect real-time and batch data from various sources such as air quality sensors, traffic monitors, weather stations, and public service systems.
- **Store Data:** Persist incoming data into a data lake, ensuring that raw, untransformed data is available for later analysis.
- **Stream Data:** Utilize Apache Kafka for real-time streaming of data between producers and consumers.
- **Machine Learning Analytics:** Build and deploy predictive models to forecast air quality, weather, traffic, and service demand.
- **Visualization:** Present analytical insights via a dashboard that visualizes trends and predictions.

This project serves as an end-to-end demonstration of modern data engineering and analytics practices, integrating multiple components into one cohesive system.

---

## Project Architecture

```plaintext
                 +---------------------+
                 |    Data Sources     |
                 | (CSV files & API)   |
                 +----------+----------+
                            │
                  [Real-time Streaming]
                            │
                 +----------▼----------+
                 |   Kafka Producer    |  ---> (producer.py)
                 +----------+----------+
                            │
                 +----------▼----------+
                 |   Kafka Consumer    |  ---> (consumer.py)
                 +----------+----------+
                            │
                 +----------▼----------+
                 |     Data Lake       |  ---> (datalake.py)
                 +----------+----------+
                            │
        +-------------------+-------------------+
        │                                       │
+-------▼-------+                      +--------▼--------+
|  Machine      |                      |  Dashboard      |
|  Learning     |                      |  (Visualization)|
| (Prediction   |                      |  (dashboard.py) |
|  APIs & Models)|                     |                 |
+-------+-------+                      +-----------------+
        │
+-------▼-------+
|   Flask App   |  ---> (app.py aggregates ML prediction endpoints)
+---------------+
```

This diagram illustrates how data flows through the system—from raw data ingestion to processing, machine learning predictions, and finally, visualization on a dashboard.

---

## Modules and File Descriptions

### Root Configuration Files

- **`.gitignore`**  
  Specifies files and directories to be ignored by Git (e.g., temporary files, virtual environments).

- **`Dockerfile`**  
  Defines the steps to build the project image. It installs required packages and sets up the Flask environment. The image is later used to run the application in a containerized environment.

- **`docker-compose.yml`**  
  Orchestrates multi-container deployment. It sets up necessary services including Zookeeper, Kafka, and the main Python application to simulate a distributed architecture.

- **`requirements.txt`**  
  Lists all Python dependencies needed for the project such as Flask, pandas, scikit-learn, kafka-python, and matplotlib.

- **`test.py`**  
  A script intended to validate core functionalities of the project (e.g., verifying data ingestion and ML predictions).

---

### Data Sources

Located in the `/Data/` directory, these files simulate raw sensor data from various city services:

- **`air_quality_data.csv`**  
  Contains sample air quality measurements including pollutants like CO2, NO2, etc.

- **`traffic_data.csv`**  
  Records simulated traffic congestion data and traffic flow metrics.

- **`weather_data.csv`**  
  Captures weather metrics (temperature, humidity, precipitation, etc.) to simulate local climate data.

- **`public_services_data.csv`**  
  Represents usage and performance metrics of public services within the city.

- **`api.py`**  
  Implements a simple Flask API to serve data from the CSV files. It provides endpoints that return random rows from each dataset, simulating a live data feed for further processing.

---

### Data Lake

- **`datalake/datalake.py`**  
  This script is responsible for acting as a basic data lake. It consumes data from Kafka topics and appends the raw data into storage files (CSV format). This ensures that all ingested data is persistently stored for future reference, analysis, or reprocessing.

---

### Streaming Infrastructure

Apache Kafka is used to handle the streaming of data in near-real time. The components are:

- **`streaming/producer.py`**  
  Reads data (often by accessing the API endpoints from `/Data/api.py`) and sends it to a Kafka topic. This simulates sensor data being produced continuously in a smart city environment.

- **`streaming/consumer.py`**  
  Listens to Kafka topics and retrieves messages produced by the producer. It may then process the data further or forward it to the data lake for storage.

---

### Machine Learning Components

This module includes training scripts, prediction scripts, and Flask APIs for serving model predictions. All ML components reside in the `/Machine_learning/` directory.

- **Air Quality Prediction**:
  - **`air-quality1.py` & `air-quality2.py`**  
    Scripts to train machine learning models (likely using techniques such as Random Forest) on air quality data. They include data preprocessing steps like label encoding and splitting into training/testing sets.
  - **`air-quality1_predict.py` & `air-quality2_predict.py`**  
    These scripts load the trained models (from serialized pickle files) and provide prediction endpoints via Flask.

- **Weather Forecasting**:
  - **`weather.py` & `weather_predict.py`**  
    Similar to air quality, these scripts handle weather data modeling. The prediction script serves forecasts for weather conditions based on input parameters.

- **Traffic Prediction**:
  - **`traffic.py` & `traffic_predict.py`**  
    Scripts that process traffic data, train predictive models, and expose endpoints to forecast traffic congestion or flow.

- **Public Service Usage Prediction**:
  - **`service.py` & `service-predict.py`**  
    These handle the modeling of public service usage, training models that predict service demand and usage trends.

- **`app.py`**  
  A unified Flask application that aggregates all prediction endpoints. This central API allows external clients (or the dashboard) to request predictions for various smart city metrics.

- **Serialized Models and Encoders**:
  - Files such as `anomaly_detection_model.pkl`, `co2_model.pkl`, `label_encoder.pkl`, and `label_encoder_service.pkl` are pre-trained models and encoders saved for fast inference during prediction tasks.

---

### Dashboard

- **`dashboard/dashboard.py`**  
  Generates visualizations using Python libraries like matplotlib and pandas. The dashboard reads data stored in the data lake and presents key trends such as:
  - Air quality over time
  - Traffic patterns and congestion levels
  - Public service usage trends
  - Weather data trends

This component is intended to provide city administrators with an intuitive interface to monitor the health and performance of various urban services.

---

## Theoretical Background

### Real-Time Data Streaming with Kafka
Apache Kafka is used to simulate the ingestion of real-time sensor data. In a real-world smart city, numerous sensors continuously generate data. Kafka allows decoupling between data producers and consumers, ensuring a resilient and scalable architecture.

### Data Lake Concept
A data lake stores vast amounts of raw data in its native format. This project simulates a data lake using CSV files where every incoming record is stored for further analysis or reprocessing. This approach provides flexibility to perform ad hoc analytics or feed machine learning pipelines.

### Machine Learning for Smart Cities
The predictive models in this project aim to forecast various parameters:
- **Air Quality Models:** Predict pollutant levels to help with environmental monitoring.
- **Weather Models:** Forecast weather conditions, aiding in city planning and emergency responses.
- **Traffic Models:** Predict traffic flows to optimize congestion management.
- **Public Services Models:** Analyze and predict usage trends to better allocate resources.

These models are built using standard machine learning techniques (e.g., RandomForestClassifier) and are trained on historical data. Their predictions can drive automated alerts and support decision-making in urban management.

### Containerization with Docker
Docker is used to package the application along with its dependencies into containers. Docker Compose further simplifies deployment by orchestrating multiple services (Kafka, Zookeeper, Flask app) to run together in a consistent environment.

---

## Installation and Setup

### Prerequisites
- **Docker & Docker Compose:** Ensure you have both installed on your machine.
- **Python 3.x:** For running scripts outside of Docker, if necessary.
- **Kafka and Zookeeper:** These will be managed via Docker Compose.

### Setup Steps
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd Smart-City_data_lake_with_Analytics-master
   ```

2. **Build Docker Containers:**
   ```bash
   docker-compose build
   ```

3. **Start the Services:**
   ```bash
   docker-compose up
   ```
   This command will start the Kafka broker, Zookeeper, and the Flask application.

4. **Install Python Dependencies Locally (Optional):**
   If running outside Docker:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Data Ingestion and Streaming
- The **API endpoints** in `Data/api.py` simulate data sources.
- Run **`streaming/producer.py`** to start sending data into Kafka.
- **`streaming/consumer.py`** listens for incoming messages and pushes data into the data lake via `datalake/datalake.py`.

### Machine Learning Predictions
- Use the prediction endpoints exposed via **`app.py`** (e.g., `/predict_air`, `/predict_weather`).
- Prediction scripts (such as `air-quality1_predict.py`) load pre-trained models and provide instant inference on input data.

### Visualization
- Launch the dashboard by running **`dashboard/dashboard.py`** to visualize trends from the data lake.

---

## Deployment with Docker

The project is designed to run in a containerized environment. Key Docker components include:

- **Dockerfile:** Defines the application image.
- **docker-compose.yml:** Manages multi-container deployment including:
  - **Kafka & Zookeeper:** For data streaming.
  - **Python Application:** Running the Flask API for ML predictions and dashboard services.

To deploy, use:
```bash
docker-compose up --build
```
This command will automatically orchestrate all services, ensuring that data flows from producers to consumers and into the data lake while exposing prediction endpoints.

---

## Testing and Future Improvements

### Testing
- **`test.py`** is provided as a simple script to verify that core functionalities (data ingestion, ML predictions) work as expected.
- Future tests could include unit tests for individual modules and integration tests across the entire pipeline.

### Future Enhancements
- **Enhanced Data Lake Storage:** Transition from CSV files to a more robust solution such as a distributed file system (e.g., HDFS, S3).
- **Advanced Analytics:** Incorporate more sophisticated anomaly detection and forecasting models.
- **User Interface:** Develop a web-based dashboard with interactive visualizations.
- **Security and Scalability:** Harden the system for production, ensuring secure data transmission and scalable deployment.

---

## License

This project is licensed under the [MIT License](LICENSE). Please refer to the LICENSE file for more details.

---

