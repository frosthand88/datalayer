import psycopg2
import random
import time
from faker import Faker
import os
from datetime import datetime, timedelta

fake = Faker()

# Allow some time for DB to be ready
time.sleep(5)

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST")
)
cur = conn.cursor()
n = 100000
nj = 1000000
start_date = datetime(2000, 1, 1)

print("Seeding base tables...")
for i in range(n):
    date = start_date + timedelta(days=i)
    cur.execute("INSERT INTO researcher (name, created_at) VALUES (%s, %s)", (fake.name(), date))
    cur.execute("INSERT INTO paper (title, created_at) VALUES (%s, %s)", (fake.sentence(nb_words=4), date))
    cur.execute("INSERT INTO topic (name, created_at) VALUES (%s, %s)", (fake.word(), date))
    cur.execute("INSERT INTO conference (name, year, created_at) VALUES (%s, %s, %s)", (fake.company(), fake.year(), date))
    cur.execute("INSERT INTO organization (name, created_at) VALUES (%s, %s)", (fake.company(), date))

print("Seeding join tables...")
for _ in range(nj):
    cur.execute("INSERT INTO researcher_paper VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT INTO paper_topic VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT INTO topic_conference VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT INTO conference_org VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, n), random.randint(1, n)))

conn.commit()
cur.close()
conn.close()
print("Data generation complete.")

