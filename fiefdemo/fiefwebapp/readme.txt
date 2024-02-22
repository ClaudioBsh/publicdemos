Short - just do it on first time once:
======================================
- run: ./scripts/onetime_get_ids.sh
- Note the ID's you got
- Update the ./config/.env (j2) file with values you note before (if not exists, create it as copy from file './config/.env.template')
- Update the ./config/jinja_vars.yml (j2) file with values you need (if not exists, create it as copy from file './config/jinja_vars.yml.template')
- That's all what you have to configure once!
- To build and start just run: ./run.sh
- Then call in a browser (or use curl or links2 when using a plain Terminal session): http://localhost
Caution: You can use FIEF (admin) without ssl/tls (https) only when using "localhost"!



Long:
======================================

Documentations:

https://www.fief.dev/
https://docs.fief.dev/
https://docs.fief.dev/self-hosting/deployment/docker-compose/
https://docs.fief.dev/integrate/python/fastapi/
https://github.com/fief-dev/fief/pkgs/container/fief => AMD64 + ARM64:-)
https://github.com/orgs/fief-dev/discussions
https://github.com/orgs/fief-dev/discussions/335 => Introduced this FIEF Demo WebApp
https://www.wheelodex.org/projects/fief-server/
https://www.wheelodex.org/projects/fief-client/

------------------------------------

SSL/TLS:
- FORWARDED_ALLOW_IPS=*
  https://docs.fief.dev/self-hosting/deployment/ssl/

------------------------------------

Stage - Production:
- All *_COOKIE_SECURE env-variables must be "True" - else you can use "False"

------------------------------------

Do not send diagnostic data:
TELEMETRY_ENABLED=false

------------------------------------

FIEF, Traefik, FastAPI, PostgreSQL:
https://github.com/orgs/fief-dev/discussions/282
https://github.com/orgs/fief-dev/discussions/299

------------------------------------

Getting ClientID, SecretID etc:
Start onetime this:
docker run -it --rm ghcr.io/fief-dev/fief:latest fief quickstart --docker
or use the ready to go script: ./scripts/onetime_get_ids.sh
Note all the ID's you got and use it within your config/.env file!

------------------------------------

HOSTS:

Have in mind, you can use FIEF without https (ssl/tls) on localhost only!

Tipp: 
If you e.g. run it on a linux terminal only machine within your local network and do you want to call it from your another machine with e.g. Windows Browser on it,
then you have to call the ip of the linux machine where your FIEFDEMO is running instead "localhost"!
And because you cannot call something like "subdomain.IP" you should use "ports:" definition for your services within docker-compose.yml,
then you can call any such service  with "IP:PORT" too.

URL-Calls (using curl, links2 from a Terminal or from a Browser if you have a GUI on your Machine):
WEB-Page:                 http://localhost
Traefik-Dashboard:        http://localhost:8080
NiceGUI                   http://api.localhost
FastAPI-Docs              http://api.localhost/docs
FIEF:                     http://fiefdemo.localhost:8000
FIEF (admin):             http://fiefdemo.localhost:8000/admin

IP-Calls (using curl, links2 from a Terminal or from a any other Browser which is available to call your machine running the FIEFDEMO):
WEB-Page:                 http://<IP>
Traefik-Dashboard:        http://<IP>:8080
NiceGUI                   http://<IP>:8001
FastAPI-Docs              http://<IP>:8001/docs
FIEF:                     http://<IP>:8000
FIEF (admin):             http://<IP>:8000/admin => will not work with FIEF-Server 0.27.0, because the need of using 'localhost' or a real domain (ssl/tls - https)!
                          Think about using 'ngrok' - more details you can find here: https://github.com/orgs/fief-dev/discussions/37

------------------------------------

