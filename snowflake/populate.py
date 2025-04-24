import snowflake.connector
import random
import time

# Snowflake connection details
sf_account = "<YOUR_ACCOUNT>"
sf_user = "<YOUR_USER>"
sf_password = "<YOUR_PASSWORD>"
sf_database = "<YOUR_DATABASE>"
sf_schema = "<YOUR_SCHEMA>"
sf_warehouse = "<YOUR_WAREHOUSE>"

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema
)

# Create a cursor
cursor = conn.cursor()

# Create schema and tables
def create_schema_and_tables():
    try:
        # Create schema if not exists
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {sf_schema};")

        # Create tables with created_at column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS researcher (
                id INT AUTOINCREMENT PRIMARY KEY,
                name STRING,
                department STRING,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paper (
                id INT AUTOINCREMENT PRIMARY KEY,
                title STRING,
                publication_year INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS author_paper (
                author_id INT,
                paper_id INT,
                PRIMARY KEY (author_id, paper_id),
                FOREIGN KEY (author_id) REFERENCES researcher(id),
                FOREIGN KEY (paper_id) REFERENCES paper(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paper_researcher (
                researcher_id INT,
                paper_id INT,
                PRIMARY KEY (researcher_id, paper_id),
                FOREIGN KEY (researcher_id) REFERENCES researcher(id),
                FOREIGN KEY (paper_id) REFERENCES paper(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("Schema and tables created successfully.")
    except Exception as e:
        print(f"Error creating schema or tables: {e}")

# Helper function to insert data into each table
def insert_data_into_table(table_name, num_rows):
    try:
        for i in range(num_rows):
            if table_name == "researcher":
                name = f"Researcher_{random.randint(1, 100000)}"
                department = random.choice(['Computer Science', 'Biology', 'Physics', 'Chemistry', 'Mathematics'])
                sql = f"""
                    INSERT INTO researcher (name, department)
                    VALUES ('{name}', '{department}');
                """
            elif table_name == "paper":
                title = f"Paper {random.randint(1, 100000)}"
                publication_year = random.randint(2000, 2025)
                sql = f"""
                    INSERT INTO paper (title, publication_year)
                    VALUES ('{title}', {publication_year});
                """
            elif table_name == "author_paper":
                author_id = random.randint(1, 100000)
                paper_id = random.randint(1, 100000)
                sql = f"""
                    INSERT INTO author_paper (author_id, paper_id)
                    VALUES ({author_id}, {paper_id});
                """
            elif table_name == "paper_researcher":
                researcher_id = random.randint(1, 100000)
                paper_id = random.randint(1, 100000)
                sql = f"""
                    INSERT INTO paper_researcher (researcher_id, paper_id)
                    VALUES ({researcher_id}, {paper_id});
                """
            cursor.execute(sql)
        print(f"Inserted {num_rows} rows into {table_name}")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")

# Create schema and tables
create_schema_and_tables()

# Insert 100k rows into each table
num_rows = 100000
insert_data_into_table('researcher', num_rows)
insert_data_into_table('paper', num_rows)
insert_data_into_table('author_paper', num_rows)
insert_data_into_table('paper_researcher', num_rows)

# Commit the transaction and close connection
conn.commit()
cursor.close()
conn.close()