import pymssql
from faker import Faker
import random
import os
import time
from datetime import datetime, timedelta

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = "frosthand_mssql_db"  # Your target database name


def wait_for_db(timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            conn = pymssql.connect(
                server="db",
                user=db_user,
                password=db_pass)
            conn.close()
            print("✅ SQL Server is up!")
            return
        except pymssql.OperationalError as e:
            print("⏳ Waiting for SQL Server to be ready...")
            time.sleep(2)
    raise TimeoutError("❌ Timed out waiting for SQL Server.")


def create_database():
    # Use a separate connection with autocommit for CREATE DATABASE
    with pymssql.connect(
        server="db",
        user=db_user,
        password=db_pass,
        autocommit=True  # ⬅️ Important!
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}')
                CREATE DATABASE {db_name}
            """)
            print(f"✅ Database '{db_name}' created or already exists.")


def create_tables(conn):
    # Create schema and tables here (add your actual schema SQL)
    cur = conn.cursor()

    print(f"📦 Creating tables in {db_name}...")

    cur.execute(f"""
        USE {db_name};
    
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='researcher' AND xtype='U')
        CREATE TABLE researcher (
            id INT PRIMARY KEY IDENTITY,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            name NVARCHAR(255) NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='paper' AND xtype='U')
        CREATE TABLE paper (
            id INT PRIMARY KEY IDENTITY,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            title NVARCHAR(255) NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='topic' AND xtype='U')
        CREATE TABLE topic (
            id INT PRIMARY KEY IDENTITY,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            name NVARCHAR(255) NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='conference' AND xtype='U')
        CREATE TABLE conference (
            id INT PRIMARY KEY IDENTITY,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            name NVARCHAR(255) NOT NULL,
            year INT NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='organization' AND xtype='U')
        CREATE TABLE organization (
            id INT PRIMARY KEY IDENTITY,
            created_at DATETIME NOT NULL DEFAULT GETDATE(),
            name NVARCHAR(255) NOT NULL
        );
        """)

    cur.execute("""
        CREATE TABLE researcher_paper (
            researcher_id INT NOT NULL,
            paper_id INT NOT NULL,
            PRIMARY KEY (researcher_id, paper_id),
            FOREIGN KEY (researcher_id) REFERENCES researcher(id),
            FOREIGN KEY (paper_id) REFERENCES paper(id)
        );
        """)

    cur.execute("""
        CREATE TABLE paper_topic (
            paper_id INT NOT NULL,
            topic_id INT NOT NULL,
            PRIMARY KEY (paper_id, topic_id),
            FOREIGN KEY (paper_id) REFERENCES paper(id),
            FOREIGN KEY (topic_id) REFERENCES topic(id)
        );
        """)

    cur.execute("""
        CREATE TABLE topic_conference (
            topic_id INT NOT NULL,
            conference_id INT NOT NULL,
            PRIMARY KEY (topic_id, conference_id),
            FOREIGN KEY (topic_id) REFERENCES topic(id),
            FOREIGN KEY (conference_id) REFERENCES conference(id)
        );
        """)

    cur.execute("""
        CREATE TABLE conference_org (
            conference_id INT NOT NULL,
            org_id INT NOT NULL,
            PRIMARY KEY (conference_id, org_id),
            FOREIGN KEY (conference_id) REFERENCES conference(id),
            FOREIGN KEY (org_id) REFERENCES organization(id)
        );
        """)

    conn.commit()
    print(f"✅ Tables created in {db_name}.")


def seed_data(conn):
    # Seed the tables with fake data
    fake = Faker()
    n = 100000
    nj = 1000000
    start_date = datetime(2000, 1, 1)

    cur = conn.cursor()

    print("Seeding base tables...")
    for i in range(n):
        date = start_date + timedelta(hours=i)
        cur.execute("INSERT INTO researcher (name, created_at) VALUES (%s, %s)", (fake.name(), date))
        cur.execute("INSERT INTO paper (title, created_at) VALUES (%s, %s)", (fake.sentence(nb_words=4), date))
        cur.execute("INSERT INTO topic (name, created_at) VALUES (%s, %s)", (fake.word(), date))
        cur.execute("INSERT INTO conference (name, year, created_at) VALUES (%s, %s, %s)",
                    (fake.company(), random.randint(2000, 2025), date))
        cur.execute("INSERT INTO organization (name, created_at) VALUES (%s, %s)", (fake.company(), date))
        if i % 10000 == 0:
            conn.commit()
    conn.commit()

    print("Seeding join tables...")
    for _ in range(nj):
        r_id = random.randint(1, n)
        p_id = random.randint(1, n)
        t_id = random.randint(1, n)
        c_id = random.randint(1, n)
        o_id = random.randint(1, n)

        cur.execute("SELECT 1 FROM researcher_paper WHERE researcher_id=%s AND paper_id=%s", (r_id, p_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO researcher_paper (researcher_id, paper_id) VALUES (%s, %s)", (r_id, p_id))

        cur.execute("SELECT 1 FROM paper_topic WHERE paper_id=%s AND topic_id=%s", (p_id, t_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO paper_topic (paper_id, topic_id) VALUES (%s, %s)", (p_id, t_id))

        cur.execute("SELECT 1 FROM topic_conference WHERE topic_id=%s AND conference_id=%s", (t_id, c_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO topic_conference (topic_id, conference_id) VALUES (%s, %s)", (t_id, c_id))

        cur.execute("SELECT 1 FROM conference_org WHERE conference_id=%s AND org_id=%s", (c_id, o_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO conference_org (conference_id, org_id) VALUES (%s, %s)", (c_id, o_id))

        if _ % 10000 == 0:
            conn.commit()
    conn.commit()


def main():
    wait_for_db()

    create_database()

    # Connect to the database and ensure the target database exists
    conn = pymssql.connect(
        server="db",
        user=db_user,
        password=db_pass
    )
    create_tables(conn)
    seed_data(conn)

    conn.close()
    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    main()