#!/bin/bash
cd ..
docker-compose -p "fiefwebapp" stop

filter="fief"

containsFilter() {
    [[ -z "$filter" || "$1" == *"$filter"* ]]
}

# Container clean
docker ps -a | grep $filter | awk '{print $1}' | xargs -I {} docker stop {}
docker ps -a | grep $filter | awk '{print $1}' | xargs -I {} docker rm {}

# Networks clean
networks=$(docker network ls -q)

for network in $networks; do
    networkName=$(docker network inspect -f '{{.Name}}' $network)
    containers=$(docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' $network)

    if [ -z "$containers" ] && containsFilter $networkName; then
        echo "Remove unused Network: $networkName"
        docker network rm $network
    fi
done

# Volumes clean
volumes=$(docker volume ls -q)

for volume in $volumes; do
    volumeName=$(docker volume inspect -f '{{.Name}}' $volume)
    containers=$(docker ps -a --filter volume=$volumeName --format "{{ .Names }}")

    if [ -z "$containers" ] && containsFilter $volumeName; then
        echo "Remove unused Volume: $volumeName"
        docker volume rm $volume
    fi
done

# Clean none images
image_ids=$(docker images | awk '/none/ {print $3}')
if [[ -z "$image_ids" ]]; then
  exit 0
fi
docker rmi $image_ids

# Remove API-Image
docker rmi fiefwebapp-api:latest
