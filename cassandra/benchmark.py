from cassandra.cluster import Cluster
import time

# Connect to Cassandra
cluster = Cluster(["localhost"])  # Assuming localhost is used
session = cluster.connect()

# Benchmark read operation
def benchmark():
    print("Starting Cassandra benchmark...\n")

    # 1. Researcher → Paper
    print(f"[1] Researcher → Paper:", end=" ")
    t0 = time.time()
    result = session.execute("SELECT paper_id FROM benchmark_keyspace.researchers LIMIT 1000")
    paper_ids = [row.paper_id for row in result]
    papers = session.execute("SELECT * FROM benchmark_keyspace.papers WHERE paper_id IN %s", (tuple(paper_ids),))
    print(f"{time.time() - t0:.2f}s")

    # 2. Researcher → Topic
    print(f"[2] Researcher → Topic:", end=" ")
    t0 = time.time()
    topic_ids = [row.topic_id for row in result]
    topics = session.execute("SELECT * FROM benchmark_keyspace.topics WHERE topic_id IN %s", (tuple(topic_ids),))
    print(f"{time.time() - t0:.2f}s")

    # 3. Researcher → Conference
    print(f"[3] Researcher → Conference:", end=" ")
    t0 = time.time()
    conf_ids = [row.conf_id for row in result]
    conferences = session.execute("SELECT * FROM benchmark_keyspace.conferences WHERE conf_id IN %s", (tuple(conf_ids),))
    print(f"{time.time() - t0:.2f}s")

    # 4. Researcher → Organization
    print(f"[4] Researcher → Organization:", end=" ")
    t0 = time.time()
    org_ids = [row.org_id for row in result]
    organizations = session.execute("SELECT * FROM benchmark_keyspace.organizations WHERE org_id IN %s", (tuple(org_ids),))
    print(f"{time.time() - t0:.2f}s")

if __name__ == "__main__":
    benchmark()
    session.shutdown()
