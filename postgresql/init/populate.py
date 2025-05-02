import psycopg2
import random
import time
from faker import Faker
import os
from datetime import datetime, timedelta
import csv

fake = Faker()

def parse_date(date_str):
    # Converts '27/10/1983' to '1983-10-27'
    return datetime.strptime(date_str, '%d/%m/%Y').date()

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

schema_sql = """
CREATE TABLE IF NOT EXISTS stock_data (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  record_date TIMESTAMP NOT NULL DEFAULT now(),
  _open NUMERIC(18,5),
  _high NUMERIC(18,5),
  _low NUMERIC(18,5),
  _close NUMERIC(18,5),
  _volume BIGINT
);

CREATE TABLE IF NOT EXISTS researcher (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL,
  age INT
);

CREATE TABLE IF NOT EXISTS paper (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS topic (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conference (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL,
  year INT
);

CREATE TABLE IF NOT EXISTS organization (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS researcher_paper (
  researcher_id INT REFERENCES researcher(id),
  paper_id INT REFERENCES paper(id),
  PRIMARY KEY (researcher_id, paper_id)
);

CREATE TABLE IF NOT EXISTS paper_topic (
  paper_id INT REFERENCES paper(id),
  topic_id INT REFERENCES topic(id),
  PRIMARY KEY (paper_id, topic_id)
);

CREATE TABLE IF NOT EXISTS topic_conference (
  topic_id INT REFERENCES topic(id),
  conference_id INT REFERENCES conference(id),
  PRIMARY KEY (topic_id, conference_id)
);

CREATE TABLE IF NOT EXISTS conference_org (
  conference_id INT REFERENCES conference(id),
  org_id INT REFERENCES organization(id),
  PRIMARY KEY (conference_id, org_id)
);
"""
print("Creating schemas...")
cur.execute(schema_sql)
conn.commit()

print("Seeding base tables...")
for i in range(n):
    date = start_date + timedelta(hours=i)
    cur.execute("INSERT INTO researcher (name, created_at, age) VALUES (%s, %s, %s)", (fake.name(), date, fake.pyint(20, 60)))
    cur.execute("INSERT INTO paper (title, created_at) VALUES (%s, %s)", (fake.sentence(nb_words=4), date))
    cur.execute("INSERT INTO topic (name, created_at) VALUES (%s, %s)", (fake.word(), date))
    cur.execute("INSERT INTO conference (name, year, created_at) VALUES (%s, %s, %s)", (fake.company(), fake.year(), date))
    cur.execute("INSERT INTO organization (name, created_at) VALUES (%s, %s)", (fake.company(), date))
    if i % 10000 == 0:
        conn.commit()
conn.commit()

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

# Example CSV filename (adjust if needed)
CSV_FILE = 'AAPL.csv'

# Extract symbol from filename
symbol = os.path.splitext(os.path.basename(CSV_FILE))[0]

with open(CSV_FILE, 'r') as f:
    reader = csv.DictReader(f)
    rows = [
        (
            symbol,
            parse_date(row['date']),
            row['open'],
            row['high'],
            row['low'],
            row['close'],
            row['volume']
        )
        for row in reader
    ]

insert_query = """
    INSERT INTO stock_data (symbol, record_date, _open, _high, _low, _close, _volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    """

cur.executemany(insert_query, rows)
conn.commit()

cur.close()
conn.close()
print("Data generation complete.")

