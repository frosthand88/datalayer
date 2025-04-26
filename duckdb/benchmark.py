import duckdb
import time

# Connect to the already populated DuckDB file
conn = duckdb.connect('research_activity.duckdb')

# Benchmark: total rows
start = time.time()
conn.execute("SELECT COUNT(*) FROM research_activity").fetchall()
print(f"COUNT(*) took {time.time() - start:.4f} seconds")

# Benchmark: filter + group
start = time.time()
conn.execute("""
    SELECT topic, AVG(citations) 
    FROM research_activity 
    WHERE time > NOW() - INTERVAL '1 day'
    GROUP BY topic
""").fetchall()
print(f"GROUP BY topic in last day took {time.time() - start:.4f} seconds")

# Benchmark: top 5 researchers
start = time.time()
conn.execute("""
    SELECT researcher, SUM(citations) as total_citations
    FROM research_activity
    GROUP BY researcher
    ORDER BY total_citations DESC
    LIMIT 5
""").fetchall()
print(f"Top 5 researchers query took {time.time() - start:.4f} seconds")

conn.close()
