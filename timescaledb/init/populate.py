import psycopg2
from datetime import datetime
import random
import time

# Retry parameters
max_retries = 5  # Number of retries
retry_delay = 5  # Delay between retries (in seconds)

# Function to establish the database connection with retries
def connect_with_retry():
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            conn = psycopg2.connect(
                host="db",  # Assuming your TimescaleDB service is named 'timescaledb' in Docker Compose
                user="admin",
                password="adminpass",
                dbname="timescale_db",
                port=5432
            )
            print("Connected to the database successfully.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to the database.")
                raise

# Establish the database connection with retry
conn = connect_with_retry()

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create the research_activity table and convert it to a hypertable
create_table_sql = """
CREATE TABLE IF NOT EXISTS research_activity (
    time TIMESTAMPTZ NOT NULL,
    researcher TEXT,
    paper TEXT,
    topic TEXT,
    conference TEXT,
    organization TEXT,
    citations INTEGER
);
"""

create_hypertable_sql = """
SELECT create_hypertable('research_activity', 'time', if_not_exists => TRUE);
"""

# Execute the table creation and hypertable conversion
cur.execute(create_table_sql)
cur.execute(create_hypertable_sql)

# Commit the changes
conn.commit()

# Sample data to insert
researchers = ["Alice", "Bob", "Charlie"]
papers = ["Paper 1", "Paper 2", "Paper 3"]
topics = ["AI", "Machine Learning", "Quantum Computing"]
conferences = ["ICML", "NeurIPS", "CVPR"]
organizations = ["University A", "Company B", "Institute C"]

# Insert some data into the research_activity table
for _ in range(100):  # Adjust the range for the number of rows you want
    time = datetime.utcnow()
    researcher = random.choice(researchers)
    paper = random.choice(papers)
    topic = random.choice(topics)
    conference = random.choice(conferences)
    organization = random.choice(organizations)
    citations = random.randint(0, 100)

    insert_sql = """
    INSERT INTO research_activity (time, researcher, paper, topic, conference, organization, citations)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(insert_sql, (time, researcher, paper, topic, conference, organization, citations))

# Commit the insertions
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data populated successfully!")
