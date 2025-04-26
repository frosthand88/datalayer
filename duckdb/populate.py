import duckdb
from datetime import datetime
import random

# Connect to DuckDB (this will create a file-based DB)
conn = duckdb.connect('research_activity.duckdb')  # This creates/opens a DuckDB file

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create the research_activity table
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

# Execute the table creation
cur.execute(create_table_sql)

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
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cur.execute(insert_sql, (time, researcher, paper, topic, conference, organization, citations))

# Commit the insertions (although DuckDB automatically commits after each statement, this is to ensure it)
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data populated successfully in DuckDB!")
