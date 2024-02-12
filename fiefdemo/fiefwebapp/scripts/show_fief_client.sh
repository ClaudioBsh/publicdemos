#!/bin/bash
echo "If you want to use another version of the fief_client, login to the container and update it manualy and/or change the requirements.txt!"
echo "Login:                      docker exec -it fief_server bash"
echo "Update fief_client:         pip install fief_client==0.18.6 --verbose"
docker exec -it fief-server pip show fief_client
