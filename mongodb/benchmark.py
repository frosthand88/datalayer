from pymongo import MongoClient
from time import perf_counter

client = MongoClient("mongodb://localhost:47017/")
db = client["bench"]

# Collections (ensure these match the collection names in MongoDB)
researchers = db.researchers
papers = db.papers
researcher_paper = db.researcher_paper
paper_topic = db.paper_topic
topics = db.topics
topic_conference = db.topic_conference
conferences = db.conferences
conference_org = db.conference_org
organizations = db.organizations

# Aggregation pipelines

pipeline1 = [
    {
        "$lookup": {
            "from": "researcher_paper",
            "localField": "_id",
            "foreignField": "researcher_id",
            "as": "rp"
        }
    },
    {"$unwind": "$rp"},
    {
        "$lookup": {
            "from": "papers",
            "localField": "rp.paper_id",
            "foreignField": "_id",
            "as": "paper"
        }
    },
    {"$unwind": "$paper"},
    {
        "$project": {
            "_id": 0,
            "researcher": "$name",
            "paper": "$paper.title"
        }
    },
    {"$limit": 1000},
]

pipeline2 = [
    {
        "$lookup": {
            "from": "researcher_paper",
            "localField": "_id",
            "foreignField": "researcher_id",
            "as": "rp"
        }
    },
    {"$unwind": "$rp"},
    {
        "$lookup": {
            "from": "papers",
            "localField": "rp.paper_id",
            "foreignField": "_id",
            "as": "paper"
        }
    },
    {"$unwind": "$paper"},
    {
        "$lookup": {
            "from": "paper_topic",
            "localField": "paper._id",
            "foreignField": "paper_id",
            "as": "pt"
        }
    },
    {"$unwind": "$pt"},
    {
        "$lookup": {
            "from": "topics",
            "localField": "pt.topic_id",
            "foreignField": "_id",
            "as": "topic"
        }
    },
    {"$unwind": "$topic"},
    {
        "$project": {
            "_id": 0,
            "researcher": "$name",
            "topic": "$topic.name"
        }
    },
    {"$limit": 1000},
]

pipeline3 = [
    {
        "$lookup": {
            "from": "researcher_paper",
            "localField": "_id",
            "foreignField": "researcher_id",
            "as": "rp"
        }
    },
    {"$unwind": "$rp"},
    {
        "$lookup": {
            "from": "papers",
            "localField": "rp.paper_id",
            "foreignField": "_id",
            "as": "paper"
        }
    },
    {"$unwind": "$paper"},
    {
        "$lookup": {
            "from": "paper_topic",
            "localField": "paper._id",
            "foreignField": "paper_id",
            "as": "pt"
        }
    },
    {"$unwind": "$pt"},
    {
        "$lookup": {
            "from": "topics",
            "localField": "pt.topic_id",
            "foreignField": "_id",
            "as": "topic"
        }
    },
    {"$unwind": "$topic"},
    {
        "$lookup": {
            "from": "topic_conference",
            "localField": "topic._id",
            "foreignField": "topic_id",
            "as": "tc"
        }
    },
    {"$unwind": "$tc"},
    {
        "$lookup": {
            "from": "conferences",
            "localField": "tc.conference_id",
            "foreignField": "_id",
            "as": "conf"
        }
    },
    {"$unwind": "$conf"},
    {
        "$project": {
            "_id": 0,
            "researcher": "$name",
            "conference": "$conf.name"
        }
    },
    {"$limit": 1000},
]

pipeline4 = [
    {"$limit": 1000},
    {
        "$lookup": {
            "from": "researcher_paper",
            "localField": "_id",
            "foreignField": "researcher_id",
            "as": "rp"
        }
    },
    {"$unwind": "$rp"},
    {
        "$lookup": {
            "from": "papers",
            "localField": "rp.paper_id",
            "foreignField": "_id",
            "as": "paper"
        }
    },
    {"$unwind": "$paper"},
    {
        "$lookup": {
            "from": "paper_topic",
            "localField": "paper._id",
            "foreignField": "paper_id",
            "as": "pt"
        }
    },
    {"$unwind": "$pt"},
    {
        "$lookup": {
            "from": "topics",
            "localField": "pt.topic_id",
            "foreignField": "_id",
            "as": "topic"
        }
    },
    {"$unwind": "$topic"},
    {
        "$lookup": {
            "from": "topic_conference",
            "localField": "topic._id",
            "foreignField": "topic_id",
            "as": "tc"
        }
    },
    {"$unwind": "$tc"},
    {
        "$lookup": {
            "from": "conferences",
            "localField": "tc.conference_id",
            "foreignField": "_id",
            "as": "conf"
        }
    },
    {"$unwind": "$conf"},
    {
        "$lookup": {
            "from": "conference_org",
            "localField": "conf._id",
            "foreignField": "conference_id",
            "as": "co"
        }
    },
    {"$unwind": "$co"},
    {
        "$lookup": {
            "from": "organizations",
            "localField": "co.org_id",
            "foreignField": "_id",
            "as": "org"
        }
    },
    {"$unwind": "$org"},
    {
        "$project": {
            "_id": 0,
            "researcher": "$name",
            "organization": "$org.name"
        }
    },
    {"$limit": 1000},
]

# Fetch 1000 researcher_ids
base_ids = researcher_paper.distinct("researcher_id")[:1000]

print("Starting Mongo benchmark...\n")

# 1. Researcher → Paper
start = perf_counter()
result = list(researchers.aggregate(pipeline1))
print(f"[1] Researcher → Paper: {perf_counter() - start:.2f}s")
print(len(result))

# 2. Researcher → Topic
start = perf_counter()
result = list(researchers.aggregate(pipeline2))
print(f"[2] Researcher → Topic: {perf_counter() - start:.2f}s")
print(len(result))

# 3. Researcher → Conference
start = perf_counter()
result = list(researchers.aggregate(pipeline3))
print(f"[3] Researcher → Conference: {perf_counter() - start:.2f}s")
print(len(result))

# 4. Researcher → Organization
start = perf_counter()
result = list(researchers.aggregate(pipeline4))
print(f"[4] Researcher → Organization: {perf_counter() - start:.2f}s")
print(len(result))
