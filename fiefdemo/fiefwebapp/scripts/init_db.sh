#!/bin/bash
set -e

# WILL BE CALLED FROM INSIDE FIEF-DB CONTAINER!

export PAGER=cat
export PGPASSWORD=$POSTGRES_PASSWORD

echo "All tables:"
psql -U $PGUSER -d $POSTGRES_DB -c "\dt"

db_exists=$(psql -U $PGUSER -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
if [ "$db_exists" = "1" ]; then
    echo "Database '$POSTGRES_DB' exists already, nothing to do - will just show max. 3 lines of any table..."
    tables=$(psql -U $PGUSER -d $POSTGRES_DB -tAc "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    for table in $tables; do
        echo "Table: $table"
        psql -U $PGUSER -d $POSTGRES_DB -c "SELECT * FROM $table LIMIT 3;"
    done
else
    echo "Database '$POSTGRES_DB' does not exist, creating it..."
    psql -U $PGUSER -c "CREATE DATABASE $POSTGRES_DB"
fi
