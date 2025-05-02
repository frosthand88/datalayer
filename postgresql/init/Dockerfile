FROM python:3.11-slim

WORKDIR /app

COPY populate.py ./
COPY AAPL.csv ./

RUN pip install psycopg2-binary faker

# Run this to allow postgres to initialize before attempting to seed
CMD ["/bin/bash", "-c", "sleep 10 && python populate.py"]
