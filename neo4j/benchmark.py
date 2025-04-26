from neo4j import GraphDatabase
import time

# Connect to Neo4j (bolt://localhost:7687)
uri = "bolt://localhost:7687"
username = "neo4j"
password = "strongpassword123"

driver = GraphDatabase.driver(uri, auth=(username, password))

def benchmark_query(tx):
    # Query to get the count of papers cited by each researcher
    result = tx.run("""
        MATCH (r:Researcher)-[:CITED]->(p:Paper)
        RETURN r.name AS researcher, COUNT(p) AS citations
        ORDER BY citations DESC
        LIMIT 10
    """)
    return result.data()

def benchmark():
    with driver.session() as session:
        start_time = time.time()
        result = session.read_transaction(benchmark_query)
        end_time = time.time()

    # Output the results
    print(f"Benchmark completed in {end_time - start_time:.4f} seconds.")
    print("Top 10 researchers by citation count:")
    for row in result:
        print(f"Researcher: {row['researcher']}, Citations: {row['citations']}")

benchmark()
