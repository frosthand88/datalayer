import psycopg2
import time

conn = psycopg2.connect(
    dbname="timescale_db",
    user="admin",
    password="adminpass",
    host="localhost",
    port=35432
)
cur = conn.cursor()

start = time.time()
cur.execute("""
    SELECT * FROM research_activity
    WHERE time > NOW() - INTERVAL '1 hour'
""")
rows = cur.fetchall()
end = time.time()

print(f"✅ Retrieved {len(rows)} rows in {end - start:.2f} seconds.")

cur.close()
conn.close()
