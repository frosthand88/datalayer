import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def benchmark(label, suffix):
    start = time.time()
    researcher_keys = r.keys("researcher:*")
    researcher_keys = [k for k in researcher_keys if ":" not in k.split(":")[-1]]  # skip rel keys
    researcher_keys = researcher_keys[:1000]  # Limit to first 1000

    pipe = r.pipeline()
    for r_key in researcher_keys:
        pipe.smembers(f"{r_key}:{suffix}")
    joined = pipe.execute()
    print(f"[{label}] Researcher → {suffix.capitalize()}: {time.time() - start:.2f}s")
    print(len(joined))

benchmark("1", "papers")
benchmark("2", "topics")
benchmark("3", "conferences")
benchmark("4", "organizations")
