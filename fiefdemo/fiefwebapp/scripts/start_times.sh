#!/bin/bash
cd ..
cd config

declare -a start_infos

for service in $(docker-compose ps -a --services); do
  container_id=$(docker-compose ps -a -q $service)
  started_at=$(docker inspect -f '{{ .State.StartedAt }}' $container_id)
  start_infos+=("$started_at|$service")
done

sorted_infos=($(printf "%s\n" "${start_infos[@]}" | sort))

echo -e "Service\t\t\t\tStarttime"
echo "------------------------------------------------------------"

for info in "${sorted_infos[@]}"; do
  IFS='|' read -r started_at service <<< "$info"
  printf "%-30s %s\n" "$service" "$started_at"
done
