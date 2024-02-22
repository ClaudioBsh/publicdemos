cd ..

if [ -f "config/.env" ]; then
  echo "using config/.env"
  echo ""
  echo "Using: FIEF_API_KEY""
  source config/.env
  #Best way using curl:
  echo "FIEF_API_KEY:       ${FIEF_API_KEY}"
  echo "ROOT_DOMAIN:        ${ROOT_DOMAIN}"
  echo "PORT:               ${PORT}"
  echo "FIEF_SERVER_URL:    ${FIEF_SERVER_URL}"
  curl -X GET -H "Authorization: Bearer ${FIEF_API_KEY}" -H "Host: ${ROOT_DOMAIN}" ${FIEF_SERVER_URL}:${PORT}/admin/api/users/ && echo "\n"

  echo "Using: FIEF_MAIN_ADMIN_API_KEY""
  source config/.env
  #Best way using curl:
  echo "FIEF_MAIN_ADMIN_API_KEY:       ${FIEF_MAIN_ADMIN_API_KEY}"
  curl -X GET -H "Authorization: Bearer ${FIEF_MAIN_ADMIN_API_KEY}" -H "Host: ${ROOT_DOMAIN}" ${FIEF_SERVER_URL}:${PORT}/admin/api/users/ && echo "\n"
else
  #Curl only will produce this: {"detail":"CANT_DETERMINE_VALID_WORKSPACE"}
  #curl http://localhost:8001
  #So better use this:
  curl http://localhost:8001/admin/api/users
fi

# Sleep to have time seeing curl response
sleep 2

# Call the fief admin url
links2 http://localhost:8001/admin/
