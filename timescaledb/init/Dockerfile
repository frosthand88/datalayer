FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY populate.py .

RUN pip install psycopg2-binary

CMD ["python", "populate.py"]
