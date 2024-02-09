#!/bin/bash
cd ..
export DOCKER_BUILDKIT=1
docker-compose -f "./docker-compose.yml" --env-file "./config/.env" --verbose build --no-cache
