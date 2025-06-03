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
    dbname="defaultdb",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=26257
)

# conn = psycopg2.connect(
    # dbname="defaultdb",
    # user=os.getenv("DB_USER"),
    # password=os.getenv("DB_PASSWORD"),
    # host=os.getenv("DB_HOST"),
    # port=26257,
    # sslmode="verify-full",
    # sslrootcert="/app/certs/ca.crt",
    # sslcert="/app/certs/client.root.crt",
    # sslkey="/app/certs/client.root.key"
# )
cur = conn.cursor()
n = 100000
nj = 1000000
start_date = datetime(2000, 1, 1)

#cur.execute("CREATE DATABASE IF NOT EXISTS bench;")
#conn.commit()
#cur.execute("SET DATABASE = bench;")
cur.execute("SET search_path TO public;")

schema_sql = """
CREATE TABLE IF NOT EXISTS researcher (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL
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
  researcher_id INT,
  paper_id INT,
  PRIMARY KEY (researcher_id, paper_id)
);

CREATE TABLE IF NOT EXISTS paper_topic (
  paper_id INT,
  topic_id INT,
  PRIMARY KEY (paper_id, topic_id)
);

CREATE TABLE IF NOT EXISTS topic_conference (
  topic_id INT,
  conference_id INT,
  PRIMARY KEY (topic_id, conference_id)
);

CREATE TABLE IF NOT EXISTS conference_org (
  conference_id INT,
  org_id INT,
  PRIMARY KEY (conference_id, org_id)
);
"""
print("Creating schemas...")
cur.execute(schema_sql)
conn.commit()

researcher_ids = []
paper_ids = []
topic_ids = []
conference_ids = []
organization_ids = []

print("Seeding base tables...")
for i in range(n):
    date = start_date + timedelta(hours=i)

    cur.execute("INSERT INTO researcher (name, created_at) VALUES (%s, %s) RETURNING id", (fake.name(), date))
    researcher_ids.append(cur.fetchone()[0])

    cur.execute("INSERT INTO paper (title, created_at) VALUES (%s, %s) RETURNING id", (fake.sentence(nb_words=4), date))
    paper_ids.append(cur.fetchone()[0])

    cur.execute("INSERT INTO topic (name, created_at) VALUES (%s, %s) RETURNING id", (fake.word(), date))
    topic_ids.append(cur.fetchone()[0])

    cur.execute("INSERT INTO conference (name, year, created_at) VALUES (%s, %s, %s) RETURNING id", (fake.company(), fake.year(), date))
    conference_ids.append(cur.fetchone()[0])

    cur.execute("INSERT INTO organization (name, created_at) VALUES (%s, %s) RETURNING id", (fake.company(), date))
    organization_ids.append(cur.fetchone()[0])

    if i % 1000 == 0:
        conn.commit()
conn.commit()

print("Seeding join tables...")
for _ in range(nj):
    cur.execute("INSERT INTO researcher_paper VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.choice(researcher_ids), random.choice(paper_ids)))
    cur.execute("INSERT INTO paper_topic VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.choice(paper_ids), random.choice(topic_ids)))
    cur.execute("INSERT INTO topic_conference VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.choice(topic_ids), random.choice(conference_ids)))
    cur.execute("INSERT INTO conference_org VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.choice(conference_ids), random.choice(organization_ids)))

conn.commit()
cur.close()
conn.close()
print("Data generation complete.")

