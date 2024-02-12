#!/bin/bash
echo "doing stop..."
./stop.sh
sleep 3
cd ..
echo "doing start..."

# Start all and us depends_on within your docker-compose.yml for an ordered start sequence
# docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d

# Start all with time to get ready - because depends_on is not good enough for this setup
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d db
sleep 8
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d redis
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d fief
sleep 25
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d worker
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d api
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d traefik
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d web

echo ""
cd scripts
./show_db.sh
echo ""
./start_times.sh
echo ""
echo "Have in mind: With each call of 'run.sh' we initialize completly new the fief database for a safe clean test!"
echo ""
