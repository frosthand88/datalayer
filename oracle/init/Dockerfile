FROM python:3.11-slim

WORKDIR /app

COPY schema.sql populate.py ./

RUN pip install oracledb faker

# Run this to allow oracle to initialize before attempting to seed
CMD ["/bin/bash", "-c", "sleep 20 && python populate.py"]
