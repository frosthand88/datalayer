import boto3
import time

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:38000', region_name='us-west-2')

def benchmark():
    print("Starting DynamoDB benchmark...\n")

    t0 = time.time()
    researchers = dynamodb.Table("Researchers").scan(Limit=1000)["Items"]
    print(f"[1] Scan Researchers: {time.time() - t0:.2f}s")

    paper_table = dynamodb.Table("Papers")
    topic_table = dynamodb.Table("Topics")
    conf_table = dynamodb.Table("Conferences")
    org_table = dynamodb.Table("Organizations")

    # Benchmark paper fetch
    t0 = time.time()
    for r in researchers:
        _ = paper_table.scan(
            FilterExpression="researcher_id = :rid",
            ExpressionAttributeValues={":rid": r["id"]}
        )
    print(f"[2] Researcher → Paper: {time.time() - t0:.2f}s")

    # Benchmark topic fetch
    t0 = time.time()
    for r in researchers:
        _ = topic_table.get_item(Key={"id": r["topic_id"]})
    print(f"[3] Researcher → Topic: {time.time() - t0:.2f}s")

    # Benchmark conference fetch
    t0 = time.time()
    for r in researchers:
        _ = conf_table.get_item(Key={"id": r["conf_id"]})
    print(f"[4] Researcher → Conference: {time.time() - t0:.2f}s")

    # Benchmark organization fetch
    t0 = time.time()
    for r in researchers:
        _ = org_table.get_item(Key={"id": r["org_id"]})
    print(f"[5] Researcher → Organization: {time.time() - t0:.2f}s")

if __name__ == "__main__":
    benchmark()
