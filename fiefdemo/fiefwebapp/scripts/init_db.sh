#!/bin/bash
set -e

#Will be called from docker-compose.yml!

# PostgreSQL-Commands, check if database exists, if not create it
export PGPASSWORD=$DATABASE_PASSWORD
db_exists=$(psql -h $DATABASE_HOST -U $DATABASE_USERNAME -tAc "SELECT 1 FROM pg_database WHERE datname='$DATABASE_NAME'")
if [ "$db_exists" = "1" ]; then
    echo "Database exists already, nothing to do..."
else
    echo "Database does not exists, creating it..."
    psql -h $DATABASE_HOST -U $DATABASE_USERNAME -c "CREATE DATABASE \"$DATABASE_NAME\""
fi
