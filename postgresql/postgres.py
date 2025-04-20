import psycopg2
import time
from pathlib import Path

QUERIES = [
    ("Researcher to Paper", """
        SELECT r.name AS researcher, p.title AS paper
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        LIMIT 1000;
    """),

    ("Researcher to Topic", """
        SELECT r.name AS researcher, t.name AS topic
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id
        LIMIT 1000;
    """),

    ("Researcher to Conference", """
        SELECT r.name AS researcher, c.name AS conference
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id
        JOIN topic_conference tc ON t.id = tc.topic_id
        JOIN conference c ON c.id = tc.conference_id
        LIMIT 1000;
    """),

    ("Researcher to Organization", """
        SELECT r.name AS researcher, o.name AS organization
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id
        JOIN topic_conference tc ON t.id = tc.topic_id
        JOIN conference c ON c.id = tc.conference_id
        JOIN conference_org co ON c.id = co.conference_id
        JOIN organization o ON o.id = co.org_id
        LIMIT 1000;
    """),
]

def run_query(cursor, name, sql):
    print(f"\n⏳ {name}...")
    start = time.perf_counter()
    cursor.execute(f"EXPLAIN ANALYZE {sql}")
    results = cursor.fetchall()
    end = time.perf_counter()
    duration = end - start

    print(f"✅ {name} took {duration:.3f} sec")
    for row in results:
        print(row[0])
    return duration

def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="frosthand_postgres_db",
        user="frosthand_postgres_username",
        password="frosthand_postgres_password"
    )
    cur = conn.cursor()

    results = []
    for name, query in QUERIES:
        duration = run_query(cur, name, query)
        results.append((name, duration))

    print("\n📊 Summary:")
    for name, dur in results:
        print(f"{name:<25} {dur:.3f} sec")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()