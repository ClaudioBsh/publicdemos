#!/bin/bash

# Find corresponding FIEF version
docker_compose_path="../docker-compose.yml"
# fief_version=$(yq e '.services.fief.image' "$docker_compose_path" | cut -d':' -f2) #yq v4.x
fief_version=$(yq r "$docker_compose_path" 'services.fief.image' | cut -d':' -f2) #yq v3.4.1
echo ""
echo "Found this FIEF Image-Version: $fief_version"
echo ""

# Do Quickstart
docker run -it --rm ghcr.io/fief-dev/fief:$fief_version fief quickstart --docker
