from elasticsearch import Elasticsearch
import time

es = Elasticsearch("http://localhost:9200")

def benchmark():
    print("Starting Elasticsearch benchmark...\n")

    result = es.search(index="researchers", body={"size": 1000, "query": {"match_all": {}}})
    researchers = result["hits"]["hits"]

    print(f"[1] Researcher → Paper:", end=" ")
    t0 = time.time()
    paper_ids = [r["_source"]["paper_id"] for r in researchers]
    papers = es.mget(index="papers", body={"ids": paper_ids})["docs"]
    print(f"{time.time() - t0:.2f}s")

    print(f"[2] Researcher → Topic:", end=" ")
    t0 = time.time()
    topic_ids = [r["_source"]["topic_id"] for r in researchers]
    topics = es.mget(index="topics", body={"ids": topic_ids})["docs"]
    print(f"{time.time() - t0:.2f}s")

    print(f"[3] Researcher → Conference:", end=" ")
    t0 = time.time()
    conf_ids = [r["_source"]["conf_id"] for r in researchers]
    confs = es.mget(index="conferences", body={"ids": conf_ids})["docs"]
    print(f"{time.time() - t0:.2f}s")

    print(f"[4] Researcher → Organization:", end=" ")
    t0 = time.time()
    org_ids = [r["_source"]["org_id"] for r in researchers]
    orgs = es.mget(index="organizations", body={"ids": org_ids})["docs"]
    print(f"{time.time() - t0:.2f}s")

if __name__ == "__main__":
    benchmark()
