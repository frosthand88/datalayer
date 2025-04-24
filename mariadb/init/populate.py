import mysql.connector
import random
import time
from faker import Faker
import os
from datetime import datetime, timedelta
from mysql.connector import OperationalError

fake = Faker()

time.sleep(20)

def connect_to_mysql():
    attempts = 0
    max_retries = 10  # Maximum number of retries
    while attempts < max_retries:
        try:
            conn_local = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database="frosthand_mariadb",
                charset='utf8mb4',
                collation='utf8mb4_general_ci'
            )
            print("Connection successful!")
            return conn_local
        except OperationalError as e:
            print(f"Connection failed. Retrying... ({attempts+1}/{max_retries})")
            time.sleep(10)  # Wait for 10 seconds before retrying
            attempts += 1

    print("Failed to connect after several attempts.")
    return None

# Try connecting to the database
conn = connect_to_mysql()

cur = conn.cursor()
n = 100000
nj = 1000000
start_date = datetime(2000, 1, 1)

print("Creating tables...")
# Create researcher table
cur.execute('''
CREATE TABLE researcher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL
);
''')

# Create paper table
cur.execute('''
CREATE TABLE IF NOT EXISTS paper (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL
);
''')

# Create topic table
cur.execute('''
CREATE TABLE topic (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL
);
''')

# Create conference table
cur.execute('''
CREATE TABLE conference (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    year INT
);
''')

# Create organization table
cur.execute('''
CREATE TABLE organization (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL
);
''')

# Create researcher_paper table
cur.execute('''
CREATE TABLE researcher_paper (
    researcher_id INT,
    paper_id INT,
    PRIMARY KEY (researcher_id, paper_id),
    FOREIGN KEY (researcher_id) REFERENCES researcher(id),
    FOREIGN KEY (paper_id) REFERENCES paper(id)
);
''')

# Create paper_topic table
cur.execute('''
CREATE TABLE paper_topic (
    paper_id INT,
    topic_id INT,
    PRIMARY KEY (paper_id, topic_id),
    FOREIGN KEY (paper_id) REFERENCES paper(id),
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);
''')

# Create topic_conference table
cur.execute('''
CREATE TABLE topic_conference (
    topic_id INT,
    conference_id INT,
    PRIMARY KEY (topic_id, conference_id),
    FOREIGN KEY (topic_id) REFERENCES topic(id),
    FOREIGN KEY (conference_id) REFERENCES conference(id)
);
''')

# Create conference_org table
cur.execute('''
CREATE TABLE conference_org (
    conference_id INT,
    org_id INT,
    PRIMARY KEY (conference_id, org_id),
    FOREIGN KEY (conference_id) REFERENCES conference(id),
    FOREIGN KEY (org_id) REFERENCES organization(id)
);
''')
conn.commit()

print("Seeding base tables...")
for i in range(n):
    date = start_date + timedelta(hours=i)
    cur.execute("INSERT INTO researcher (name, created_at) VALUES (%s, %s)", (fake.name(), date))
    cur.execute("INSERT INTO paper (title, created_at) VALUES (%s, %s)", (fake.sentence(nb_words=4), date))
    cur.execute("INSERT INTO topic (name, created_at) VALUES (%s, %s)", (fake.word(), date))
    cur.execute("INSERT INTO conference (name, year, created_at) VALUES (%s, %s, %s)", (fake.company(), fake.year(), date))
    cur.execute("INSERT INTO organization (name, created_at) VALUES (%s, %s)", (fake.company(), date))
    if i % 10000 == 0:
        conn.commit()
conn.commit()

print("Seeding join tables...")
for _ in range(nj):
    cur.execute("INSERT IGNORE INTO researcher_paper VALUES (%s, %s)", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT IGNORE INTO paper_topic VALUES (%s, %s)", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT IGNORE INTO topic_conference VALUES (%s, %s)", (
        random.randint(1, n), random.randint(1, n)))
    cur.execute("INSERT IGNORE INTO conference_org VALUES (%s, %s)", (
        random.randint(1, n), random.randint(1, n)))

conn.commit()
cur.close()
conn.close()
print("Data generation complete.")

