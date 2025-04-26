from neo4j import GraphDatabase
import random
from datetime import datetime

# Connect to Neo4j (bolt://localhost:7687)
uri = "bolt://localhost:7687"
username = "neo4j"
password = "strongpassword123"

driver = GraphDatabase.driver(uri, auth=(username, password))


def create_data(tx):
    researchers = ["Alice", "Bob", "Charlie"]
    papers = ["Paper 1", "Paper 2", "Paper 3"]
    topics = ["AI", "Machine Learning", "Quantum Computing"]

    # Create some researcher nodes and paper nodes, plus relationships
    for _ in range(100):
        researcher = random.choice(researchers)
        paper = random.choice(papers)
        topic = random.choice(topics)
        citation_count = random.randint(0, 100)

        # Create researcher and paper nodes, plus a relationship (CITED)
        tx.run("""
            MERGE (r:Researcher {name: $researcher})
            MERGE (p:Paper {title: $paper, topic: $topic})
            MERGE (r)-[:CITED]->(p)
            SET p.citations = $citations
        """, researcher=researcher, paper=paper, topic=topic, citations=citation_count)


def populate():
    with driver.session() as session:
        session.write_transaction(create_data)
    print("Data populated successfully!")


populate()
