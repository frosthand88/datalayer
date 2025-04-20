import psycopg2
import random
import time
from faker import Faker
import os

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

print("Seeding base tables...")
for _ in range(1000):
    cur.execute("INSERT INTO researcher (name) VALUES (%s)", (fake.name(),))
    cur.execute("INSERT INTO paper (title) VALUES (%s)", (fake.sentence(nb_words=4),))
    cur.execute("INSERT INTO topic (name) VALUES (%s)", (fake.word(),))
    cur.execute("INSERT INTO conference (name, year) VALUES (%s, %s)", (fake.company(), fake.year()))
    cur.execute("INSERT INTO organization (name) VALUES (%s)", (fake.company(),))

print("Seeding join tables...")
for _ in range(10000):
    cur.execute("INSERT INTO researcher_paper VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, 1000), random.randint(1, 1000)))
    cur.execute("INSERT INTO paper_topic VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, 1000), random.randint(1, 1000)))
    cur.execute("INSERT INTO topic_conference VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, 1000), random.randint(1, 1000)))
    cur.execute("INSERT INTO conference_org VALUES (%s, %s) ON CONFLICT DO NOTHING", (
        random.randint(1, 1000), random.randint(1, 1000)))

conn.commit()
cur.close()
conn.close()
print("Data generation complete.")

