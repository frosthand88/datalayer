from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
import random
import uuid
from datetime import datetime

# Connect to Cassandra
cluster = Cluster(["localhost"])  # Assuming localhost is used
cluster.connection_class = LibevConnection
session = cluster.connect()

# Create keyspace and tables if they don't exist
session.execute("""
CREATE KEYSPACE IF NOT EXISTS benchmark_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")

session.execute("""
CREATE TABLE IF NOT EXISTS benchmark_keyspace.researchers (
    researcher_id UUID PRIMARY KEY,
    name TEXT,
    paper_id UUID,
    topic_id UUID,
    conf_id UUID,
    org_id UUID
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS benchmark_keyspace.papers (
    paper_id UUID PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS benchmark_keyspace.topics (
    topic_id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS benchmark_keyspace.conferences (
    conf_id UUID PRIMARY KEY,
    name TEXT,
    year INT,
    created_at TIMESTAMP
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS benchmark_keyspace.organizations (
    org_id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP
)
""")

# Insert dummy data into each table
def populate_data(n=1000):
    for _ in range(n):
        # Generate UUIDs for paper, topic, conf, and org for relational integrity
        paper_id = uuid.uuid4()
        topic_id = uuid.uuid4()
        conf_id = uuid.uuid4()
        org_id = uuid.uuid4()

        # Inserting data into papers, topics, conferences, and organizations
        session.execute("""
        INSERT INTO benchmark_keyspace.papers (paper_id, title, created_at)
        VALUES (%s, %s, %s)
        """, (paper_id, f"Paper {random.randint(1, 10000)}", datetime.utcnow()))

        session.execute("""
        INSERT INTO benchmark_keyspace.topics (topic_id, name, created_at)
        VALUES (%s, %s, %s)
        """, (topic_id, f"Topic {random.randint(1, 10000)}", datetime.utcnow()))

        session.execute("""
        INSERT INTO benchmark_keyspace.conferences (conf_id, name, year, created_at)
        VALUES (%s, %s, %s, %s)
        """, (conf_id, f"Conference {random.randint(1, 10000)}", random.randint(2000, 2025), datetime.utcnow()))

        session.execute("""
        INSERT INTO benchmark_keyspace.organizations (org_id, name, created_at)
        VALUES (%s, %s, %s)
        """, (org_id, f"Organization {random.randint(1, 10000)}", datetime.utcnow()))

        # Inserting data into researchers with relationships to the other tables
        session.execute("""
        INSERT INTO benchmark_keyspace.researchers (researcher_id, name, paper_id, topic_id, conf_id, org_id)
        VALUES (uuid(), %s, %s, %s, %s, %s)
        """, (f"Researcher {random.randint(1, 10000)}", paper_id, topic_id, conf_id, org_id))

if __name__ == "__main__":
    print("Populating data...")
    populate_data()
    print("Data populated successfully!")
    session.shutdown()
