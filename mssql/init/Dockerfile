FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    freetds-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pymssql (works with SQL Server, no ODBC required)
RUN pip install pymssql faker

# Copy code
COPY populate.py /app/populate.py
WORKDIR /app

CMD ["python", "populate.py"]