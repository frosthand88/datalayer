docker run -d \
  -e POSTGRES_USER=frosthand_postgres_username \
  -e POSTGRES_PASSWORD=frosthand_postgres_password \
  -e POSTGRES_DB=frosthand_postgres_db \
  -p 5432:5432 \
  postgres:14.17