import boto3
from faker import Faker
import uuid

fake = Faker()

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:38000', region_name='us-west-2')

tables = ["Researchers", "Papers", "Topics", "Conferences", "Organizations"]

def create_tables():
    for name in tables:
        try:
            table = dynamodb.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
            )
            table.wait_until_exists()
            print(f"Created table: {name}")
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"Table already exists: {name}")

def populate_data(n=1000):
    topics = []
    conferences = []
    organizations = []

    # Populate base tables first
    for _ in range(20):
        topic_id = str(uuid.uuid4())
        dynamodb.Table("Topics").put_item(Item={"id": topic_id, "name": fake.word()})
        topics.append(topic_id)

        conf_id = str(uuid.uuid4())
        dynamodb.Table("Conferences").put_item(Item={"id": conf_id, "name": fake.company()})
        conferences.append(conf_id)

        org_id = str(uuid.uuid4())
        dynamodb.Table("Organizations").put_item(Item={"id": org_id, "name": fake.company()})
        organizations.append(org_id)

    researchers = []
    for _ in range(n):
        researcher_id = str(uuid.uuid4())
        topic_id = fake.random_element(topics)
        conf_id = fake.random_element(conferences)
        org_id = fake.random_element(organizations)

        dynamodb.Table("Researchers").put_item(Item={
            "id": researcher_id,
            "name": fake.name(),
            "topic_id": topic_id,
            "conf_id": conf_id,
            "org_id": org_id
        })
        researchers.append(researcher_id)

        # Each researcher writes a paper
        paper_id = str(uuid.uuid4())
        dynamodb.Table("Papers").put_item(Item={
            "id": paper_id,
            "title": fake.sentence(nb_words=6),
            "researcher_id": researcher_id
        })

if __name__ == "__main__":
    create_tables()
    populate_data()
