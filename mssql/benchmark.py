import pyodbc
import time
import os

QUERIES = [
    ("Researcher to Paper", """
        SELECT TOP 1000 r.name AS researcher, p.title AS paper
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id;
    """),

    ("Researcher to Topic", """
        SELECT TOP 1000 r.name AS researcher, t.name AS topic
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id;
    """),

    ("Researcher to Conference", """
        SELECT TOP 1000 r.name AS researcher, c.name AS conference
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id
        JOIN topic_conference tc ON t.id = tc.topic_id
        JOIN conference c ON c.id = tc.conference_id;
    """),

    ("Researcher to Organization", """
        SELECT TOP 1000 r.name AS researcher, o.name AS organization
        FROM researcher r
        JOIN researcher_paper rp ON r.id = rp.researcher_id
        JOIN paper p ON p.id = rp.paper_id
        JOIN paper_topic pt ON p.id = pt.paper_id
        JOIN topic t ON t.id = pt.topic_id
        JOIN topic_conference tc ON t.id = tc.topic_id
        JOIN conference c ON c.id = tc.conference_id
        JOIN conference_org co ON c.id = co.conference_id
        JOIN organization o ON o.id = co.org_id;
    """),
]

def run_query(cursor, name, sql):
    print(f"\n⏳ {name}...")
    # SQL Server doesn't support LIMIT — replace with TOP
    start = time.perf_counter()
    cursor.execute(sql)
    results = cursor.fetchall()
    end = time.perf_counter()
    duration = end - start

    print(f"✅ {name} took {duration:.3f} sec")
    for row in results[:3]:  # limit terminal spam
        print(row)
    return duration

def main():
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                          f"SERVER=localhost,1433;"
                          f"DATABASE=frosthand_mssql_db;"
                          f"UID=sa;"
                          f"PWD=frosthand_mssql_password123*!")
    cursor = conn.cursor()

    results = []
    for name, query in QUERIES:
        duration = run_query(cursor, name, query)
        results.append((name, duration))

    print("\n📊 Summary:")
    for name, dur in results:
        print(f"{name:<25} {dur:.3f} sec")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()