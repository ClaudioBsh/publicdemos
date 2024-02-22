#!/bin/bash

cd scripts

if [ ! -f ../config/.env ]; then
  echo "Caution: 'config/.env' file does not exist! Create it as copy of 'config/.env.template', configure it (you need to run 'scripts/onetime_get_ids.sh' before!), then repeat this script!"
  exit 1
fi

if [ ! -f ../config/jinja_vars.yml ]; then
  echo "Caution: 'config/jinja_vars.yml' file does not exist! Create it as copy of 'config/jinja_vars.yml.template', configure it, then repeat this script!"
  exit 1
fi

echo "doing stop..."
./stop.sh
sleep 3

echo "check install..."
./install.sh

echo "doing jinja..."
./process_jinja.sh"

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
