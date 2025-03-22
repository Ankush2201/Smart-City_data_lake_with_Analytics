from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from pymongo import MongoClient
import pandas as pd

# Initialize Dash app
app = Dash(__name__)
app.title = "Smart City Dashboard"

# MongoDB client and database
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "smart_city"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("Smart City Dashboard", style={"textAlign": "center"}),

        html.Div([
            html.Div([dcc.Graph(id="traffic-speed-graph")], className="six columns"),
            html.Div([dcc.Graph(id="weather-temperature-graph")], className="six columns"),
        ], className="row"),

        html.Div([
            html.Div([dcc.Graph(id="air-quality-graph")], className="six columns"),
            html.Div([dcc.Graph(id="public-services-usage-graph")], className="six columns"),
        ], className="row"),

        html.Div([
            html.Div([dcc.Graph(id="weather-rainfall-graph")], className="six columns"),
        ], className="row"),

        # New Row for Additional Graphs
        html.Div([
            html.Div([dcc.Graph(id="traffic-2d-scatter-graph")], className="six columns"),
            html.Div([dcc.Graph(id="public-services-sunburst-graph")], className="six columns"),
        ], className="row"),

        html.Div([
            html.Div([dcc.Graph(id="traffic-candlestick-graph")], className="six columns"),
        ], className="row"),
    ]),
    # Set Interval component for real-time updates (10 seconds)
    dcc.Interval(id="interval-component", interval=10000, n_intervals=0)
], style={"padding": "20px"})

# Define schema and casting functions
traffic_casts = {
    "average_speed": float,
    "congestion_level": str,
    "timestamp": str,
    "vehicle_count": int
}

weather_casts = {
    "humidity": int,
    "location": str,
    "rainfall": float,
    "temperature": float,
    "timestamp": str,
    "wind_speed": float
}

air_quality_casts = {
    "co2": float,
    "location": str,
    "pm10": float,
    "pm25": float,
    "timestamp": str
}

public_services_casts = {
    "service": str,
    "status": str,
    "timestamp": str,
    "usage": float
}

# Function to fetch and cast data from MongoDB
def fetch_and_cast_data(collection_name, casts, limit=50):
    collection = db[collection_name]
    data_cursor = collection.find().sort("_id", -1).limit(limit)
    data = list(data_cursor)
    df = pd.DataFrame(data)
   
    # Cast the columns according to the schema
    for column, dtype in casts.items():
        if column in df.columns:
            df[column] = df[column].apply(lambda x: dtype(x) if pd.notnull(x) else None)
   
    return df

# Traffic speed graph (Scatter Plot)
@app.callback(
    Output("traffic-speed-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_traffic_speed_graph(n):
    data = fetch_and_cast_data("traffic", traffic_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    avg_speeds = data["average_speed"]

    # Use a scatter plot for traffic speed visualization
    figure = go.Figure([go.Scatter(x=timestamps, y=avg_speeds, mode="markers", name="Average Speed", marker=dict(color="blue"))])
    figure.update_layout(title="Traffic: Average Speed", xaxis_title="Time", yaxis_title="Speed (km/h)")
    return figure

# Weather temperature graph (Scatter Plot)
@app.callback(
    Output("weather-temperature-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_weather_temperature_graph(n):
    data = fetch_and_cast_data("weather", weather_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    temperatures = data["temperature"]

    # Use a scatter plot for temperature visualization
    figure = go.Figure([go.Scatter(x=timestamps, y=temperatures, mode="markers", name="Temperature", marker=dict(color="orange"))])
    figure.update_layout(title="Weather: Temperature Over Time", xaxis_title="Time", yaxis_title="Temperature (°C)")
    return figure

# Air quality graph (Bar Chart)
@app.callback(
    Output("air-quality-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_air_quality_graph(n):
    data = fetch_and_cast_data("air_quality", air_quality_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    pm25 = data["pm25"]

    figure = go.Figure([go.Bar(x=timestamps, y=pm25, name="PM2.5 Levels", marker=dict(color="orange"))])
    figure.update_layout(title="Air Quality: PM2.5 Levels", xaxis_title="Time", yaxis_title="PM2.5 (µg/m³)")
    return figure

# Public services usage graph (Pie Chart)
@app.callback(
    Output("public-services-usage-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_public_services_usage_graph(n):
    data = fetch_and_cast_data("public_services", public_services_casts)
    if data.empty:
        return go.Figure()

    services = data["service"]
    usage = data["usage"]

    figure = go.Figure([go.Pie(labels=services, values=usage, hole=0.4)])
    figure.update_layout(title="Public Services Usage Distribution")
    return figure

# Weather rainfall graph (Line Plot)
@app.callback(
    Output("weather-rainfall-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_weather_rainfall_graph(n):
    data = fetch_and_cast_data("weather", weather_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    rainfall = data["rainfall"]

    figure = go.Figure([go.Scatter(x=timestamps, y=rainfall, mode="lines", name="Rainfall", line=dict(color="blue"))])
    figure.update_layout(title="Weather: Rainfall Over Time", xaxis_title="Time", yaxis_title="Rainfall (mm)")
    return figure

# 2D Traffic data visualization (2D Scatter Plot)
@app.callback(
    Output("traffic-2d-scatter-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_traffic_2d_scatter_graph(n):
    data = fetch_and_cast_data("traffic", traffic_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    vehicle_count = data["vehicle_count"]
    avg_speeds = data["average_speed"]

    figure = go.Figure([go.Scatter(
        x=vehicle_count,
        y=avg_speeds,
        mode="markers",
        marker=dict(size=8, color=avg_speeds, colorscale="Viridis", opacity=0.7)
    )])
    figure.update_layout(title="2D Traffic Visualization", xaxis_title="Vehicle Count", yaxis_title="Average Speed (km/h)")
    return figure

# Public services usage (Sunburst Chart)
@app.callback(
    Output("public-services-sunburst-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_public_services_sunburst_graph(n):
    data = fetch_and_cast_data("public_services", public_services_casts)
    if data.empty:
        return go.Figure()

    services = data["service"]
    usage = data["usage"]

    figure = go.Figure(go.Sunburst(
        labels=services,
        parents=[""]*len(services),
        values=usage,
        branchvalues="total"
    ))
    figure.update_layout(title="Public Services Usage Distribution (Sunburst)")
    return figure

# Candlestick Plot for Traffic Data
@app.callback(
    Output("traffic-candlestick-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_traffic_candlestick_graph(n):
    data = fetch_and_cast_data("traffic", traffic_casts)
    if data.empty:
        return go.Figure()

    timestamps = pd.to_datetime(data["timestamp"])
    vehicle_count = data["vehicle_count"]
    avg_speeds = data["average_speed"]

    figure = go.Figure([go.Candlestick(
        x=timestamps,
        open=vehicle_count,
        high=vehicle_count,
        low=avg_speeds,
        close=avg_speeds,
        increasing_line_color="green",
        decreasing_line_color="red"
    )])
    figure.update_layout(title="Traffic Candlestick Plot", xaxis_title="Time", yaxis_title="Vehicle Count / Speed")
    return figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)