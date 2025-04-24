from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
client = MongoClient("mongodb://db:27017/")
db = client["bench"]

n = 100_000
nj = 200_000
start_date = datetime.utcnow()

# Collections
researchers = db.researchers
papers = db.papers
topics = db.topics
conferences = db.conferences
organizations = db.organizations
researcher_paper = db.researcher_paper
paper_topic = db.paper_topic
topic_conference = db.topic_conference
conference_org = db.conference_org

print("Seeding base collections...")

researcher_ids = []
paper_ids = []
topic_ids = []
conference_ids = []
org_ids = []

for i in range(n):
    date = start_date + timedelta(seconds=i)
    r_id = researchers.insert_one({"name": fake.name(), "created_at": date}).inserted_id
    p_id = papers.insert_one({"title": fake.sentence(nb_words=4), "created_at": date}).inserted_id
    t_id = topics.insert_one({"name": fake.word(), "created_at": date}).inserted_id
    c_id = conferences.insert_one({"name": fake.company(), "year": fake.year(), "created_at": date}).inserted_id
    o_id = organizations.insert_one({"name": fake.company(), "created_at": date}).inserted_id

    researcher_ids.append(r_id)
    paper_ids.append(p_id)
    topic_ids.append(t_id)
    conference_ids.append(c_id)
    org_ids.append(o_id)

print("Seeding join collections...")

for _ in range(nj):
    researcher_paper.insert_one({
        "researcher_id": random.choice(researcher_ids),
        "paper_id": random.choice(paper_ids)
    })
    paper_topic.insert_one({
        "paper_id": random.choice(paper_ids),
        "topic_id": random.choice(topic_ids)
    })
    topic_conference.insert_one({
        "topic_id": random.choice(topic_ids),
        "conference_id": random.choice(conference_ids)
    })
    conference_org.insert_one({
        "conference_id": random.choice(conference_ids),
        "org_id": random.choice(org_ids)
    })

print("Done seeding.")