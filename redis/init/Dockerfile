FROM python:3.11-slim

WORKDIR /app

COPY populate.py .

RUN pip install redis faker

CMD ["python", "populate.py"]
