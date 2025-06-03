from elasticsearch import Elasticsearch
from faker import Faker
from datetime import datetime
import logging
import random
from dotenv import load_dotenv
import os

# Load variables from .env file into environment
load_dotenv(dotenv_path=".env")  # defaults to .env in current dir

logging.basicConfig(level=logging.DEBUG)

fake = Faker()
username = os.getenv("ELASTIC_USER")
password = os.getenv("ELASTIC_PASSWORD")

# Connect to Elasticsearch
es = Elasticsearch(
    "http://localhost:9200",
    http_auth=(username, password),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

# Define index names (must be lowercase!)
indices = ["researchers", "papers", "topics", "conferences", "organizations"]

print("Elasticsearch version:", es.info().body["version"]["number"])


# Create indices if they don't exist
def create_indices():
    for index in indices:
        if not es.indices.exists(index=index):
            es.indices.create(index=index)
            print(f"Created index: {index}")
        else:
            print(f"Index already exists: {index}")


# Populate data
def populate_data(n=1000):
    paper_ids = []  # To store paper IDs and reference them in researcher data
    topic_ids = []  # To store topic IDs and reference them in researcher data
    conf_ids = []  # To store conference IDs and reference them in researcher data
    org_ids = []  # To store organization IDs and reference them in researcher data

    for _ in range(n):
        date = datetime.utcnow().isoformat()

        # Create a paper document with a unique ID (paper_id)
        paper_id = fake.uuid4()  # Generate a unique paper_id for each paper
        paper = {
            "title": fake.sentence(nb_words=4),
            "created_at": date,
            "paper_id": paper_id  # Add paper_id field here
        }
        es.index(index="papers", document=paper)

        # Store the paper_id for use in researchers
        paper_ids.append(paper_id)

        # Create a topic document and store topic_id
        topic_id = fake.uuid4()  # Generate a unique topic_id for each topic
        topic = {
            "name": fake.word(),
            "created_at": date,
            "topic_id": topic_id  # Add topic_id field here
        }
        es.index(index="topics", document=topic)

        # Store the topic_id for use in researchers
        topic_ids.append(topic_id)

        # Create a conference document and store conf_id
        conf_id = fake.uuid4()  # Generate a unique conf_id for each conference
        conference = {
            "name": fake.company(),
            "year": fake.year(),
            "created_at": date,
            "conf_id": conf_id  # Add conf_id field here
        }
        es.index(index="conferences", document=conference)

        # Store the conf_id for use in researchers
        conf_ids.append(conf_id)

        # Create an organization document and store org_id
        org_id = fake.uuid4()  # Generate a unique org_id for each organization
        organization = {
            "name": fake.company(),
            "created_at": date,
            "org_id": org_id  # Add org_id field here
        }
        es.index(index="organizations", document=organization)

        # Store the org_id for use in researchers
        org_ids.append(org_id)

        # Create a researcher document and link to paper_id, topic_id, conf_id, org_id
        researcher = {
            "name": fake.name(),
            "created_at": date,
            "paper_id": random.choice(paper_ids),  # Link researcher to a paper
            "topic_id": random.choice(topic_ids),  # Link researcher to a topic
            "conf_id": random.choice(conf_ids),  # Link researcher to a conference
            "org_id": random.choice(org_ids)  # Link researcher to an organization
        }
        es.index(index="researchers", document=researcher)


if __name__ == "__main__":
    create_indices()
    populate_data()
