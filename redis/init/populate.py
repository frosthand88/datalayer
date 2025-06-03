import redis
from faker import Faker
from datetime import datetime
import random
import os

password = os.environ['REDIS_PASSWORD']

r = redis.Redis(host='redis', port=6379, password=password, decode_responses=True)
fake = Faker()

NUM_RECORDS = 200000

for i in range(NUM_RECORDS):
    researcher_id = f"researcher:{i}"
    paper_id = f"paper:{i}"
    topic_id = f"topic:{i}"
    conf_id = f"conference:{i}"
    org_id = f"organization:{i}"

    r.hset(researcher_id, mapping={
        "name": fake.name(),
        "created_at": str(datetime.utcnow())
    })

    r.hset(paper_id, mapping={
        "title": fake.sentence(nb_words=4),
        "created_at": str(datetime.utcnow())
    })
    r.hset(topic_id, mapping={"name": fake.word()})
    r.hset(conf_id, mapping={"name": fake.company(), "year": fake.year()})
    r.hset(org_id, mapping={"name": fake.company()})

    r.sadd(f"{researcher_id}:papers", paper_id)
    r.sadd(f"{researcher_id}:topics", topic_id)
    r.sadd(f"{researcher_id}:conferences", conf_id)
    r.sadd(f"{researcher_id}:organizations", org_id)

    if i % 10000 == 0:
        print(f"Inserted {i} records...")
