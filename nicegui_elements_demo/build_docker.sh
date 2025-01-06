# Stop App
docker stop myniceguidemo
docker rm myniceguidemo

# Build App
docker build -t myniceguidemo .

#Clean - Start
# Filtern und extrahieren der Image-IDs der Images mit dem Tag "none"
image_ids=$(docker images | awk '/none/ {print $3}')

if [[ -z "$image_ids" ]]; then
  echo "Keine Docker-Images mit dem Tag 'none' gefunden."
  exit 0
fi

# Entfernen der Images mit den entsprechenden Image-IDs
docker rmi $image_ids

# Überprüfen, ob das Entfernen erfolgreich war
if [[ $? -eq 0 ]]; then
  echo "Docker-Images mit dem Tag 'none' erfolgreich entfernt."
else
  echo "Fehler beim Entfernen der Docker-Images mit dem Tag 'none'."
fi
# Clean - End
