#!/bin/bash
cd ..
echo "doing stop..."
docker-compose -p "fiefwebapp" stop
echo "doing start..."
docker-compose -p "fiefwebapp" --env-file "./config/.env" up --build -d
