from influxdb_client import InfluxDBClient
import time

url = "http://localhost:38086"
token = "mytoken"
org = "myorg"
bucket = "mybucket"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

query = f'''
from(bucket: "{bucket}")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "research_activity")
'''

start = time.time()
tables = query_api.query(query)
count = 0

for table in tables:
    for row in table.records:
        count += 1

end = time.time()
print(f"✅ Retrieved {count} records in {end - start:.2f} seconds.")
