from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
import logging
import os
import pymongo  # MongoDB driver

# Set HADOOP_HOME and update PATH
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += os.pathsep + os.path.join(os.environ["HADOOP_HOME"], "bin")

os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "smart_city"

# Kafka Configuration
KAFKA_BROKER = "localhost:9094"
TOPICS = {
    "traffic": "traffic_topic",
    "weather": "weather_topic",
    "air_quality": "air_quality_topic",
    "public_services": "public_services_topic"
}

# Define schemas for each data type (alphabetically arranged fields)
traffic_schema = StructType([
    StructField("average_speed", StringType(), True),
    StructField("congestion_level", StringType(), True),
    StructField("location", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("vehicle_count", StringType(), True)
])

weather_schema = StructType([
    StructField("humidity", StringType(), True),
    StructField("location", StringType(), True),
    StructField("rainfall", StringType(), True),
    StructField("temperature", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("wind_speed", StringType(), True)
])

air_quality_schema = StructType([
    StructField("co2", StringType(), True),
    StructField("location", StringType(), True),
    StructField("pm10", StringType(), True),
    StructField("pm25", StringType(), True),
    StructField("timestamp", StringType(), True)
])

public_services_schema = StructType([
    StructField("service", StringType(), True),
    StructField("status", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("usage", StringType(), True)
])

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("SmartCityDataProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to read data from Kafka and handle type casting
def read_from_kafka(topic, schema, column_casts):
    # Read and parse the JSON data
    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .load() \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Cast columns to the specified data types
    for col_name, data_type in column_casts.items():
        raw_df = raw_df.withColumn(col_name, col(col_name).cast(data_type))

    return raw_df

# Write data to MongoDB
def write_to_mongo(batch_df, batch_id, collection_name):
    """Write DataFrame to MongoDB collection."""
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[collection_name]
    
    # Convert DataFrame to JSON
    data = batch_df.toJSON().collect()
    if data:
        json_data = [eval(record) for record in data]  # Convert JSON strings to Python dicts
        collection.insert_many(json_data)
        logger.info(f"Batch {batch_id} written to MongoDB collection: {collection_name}")

# Define the column casts for each topic
traffic_casts = {
    "average_speed": "float",
    "congestion_level": "string",
    "location": "string",
    "timestamp": "string",
    "vehicle_count": "int"
}

weather_casts = {
    "humidity": "int",
    "location": "string",
    "rainfall": "float",
    "temperature": "float",
    "timestamp": "string",
    "wind_speed": "float"
}

air_quality_casts = {
    "co2": "float",
    "location": "string",
    "pm10": "float",
    "pm25": "float",
    "timestamp": "string"
}

public_services_casts = {
    "service": "string",
    "status": "string",
    "timestamp": "string",
    "usage": "float"
}

# Read and process data from Kafka topics with the updated function
traffic_df = read_from_kafka(TOPICS["traffic"], traffic_schema, traffic_casts)
weather_df = read_from_kafka(TOPICS["weather"], weather_schema, weather_casts)
air_quality_df = read_from_kafka(TOPICS["air_quality"], air_quality_schema, air_quality_casts)
public_services_df = read_from_kafka(TOPICS["public_services"], public_services_schema, public_services_casts)

# Attach the MongoDB write operation to each stream
traffic_df.writeStream.foreachBatch(lambda df, id: write_to_mongo(df, id, "traffic")).start()
weather_df.writeStream.foreachBatch(lambda df, id: write_to_mongo(df, id, "weather")).start()
air_quality_df.writeStream.foreachBatch(lambda df, id: write_to_mongo(df, id, "air_quality")).start()
public_services_df.writeStream.foreachBatch(lambda df, id: write_to_mongo(df, id, "public_services")).start()

# Await termination
spark.streams.awaitAnyTermination()
