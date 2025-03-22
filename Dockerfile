# Use a Python base image
FROM python:3.9-slim

# Install Java for Spark
RUN apt-get update && apt-get install -y openjdk-11-jre-headless

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set working directory in the container
WORKDIR /streaming

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Default command (can be overridden by docker-compose.yml)
CMD ["python", "streaming/producer.py"]