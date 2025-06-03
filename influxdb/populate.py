from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
import random
from dotenv import load_dotenv
import os

# Load variables from .env file into environment
load_dotenv(dotenv_path=".env")  # defaults to .env in current dir

url = "http://localhost:38086"
token = os.getenv("INFLUX_PASSWORD")
org = "myorg"
bucket = "mybucket"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

researchers = ["Alice", "Bob", "Charlie", "Diana"]
papers = ["Quantum DB", "AI Reasoning", "Graph Computation", "Edge Systems"]
topics = ["Databases", "AI", "Networks", "Security"]
conferences = ["VLDB", "NeurIPS", "SIGCOMM", "IEEE S&P"]
organizations = ["MIT", "Stanford", "Google", "Meta"]

for i in range(100):
    r = random.choice(researchers)
    p = random.choice(papers)
    t = random.choice(topics)
    c = random.choice(conferences)
    o = random.choice(organizations)

    point = (
        Point("research_activity")
        .tag("researcher", r)
        .tag("paper", p)
        .tag("topic", t)
        .tag("conference", c)
        .tag("organization", o)
        .field("citations", random.randint(10, 1000))
        .time(datetime.now(timezone.utc), WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)

print("✅ InfluxDB populated with research data.")
