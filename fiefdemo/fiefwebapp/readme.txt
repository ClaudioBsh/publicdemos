Short - just do it on first time once:
======================================
- run: ./scripts/onetime_get_ids.sh
- Note the ID's you got
- Update the ./config/.env file with values you note before (if not exists, create it as copy from file './config/.env.template')
- Edit /etc/hosts or on Windows the Windows hosts file (see comments below in the "Long:" Section - Chapter "HOSTS:" => nearly at the end of this document)
- That's all what you have to configure once!
- To build and start just run: ./scripts/run.sh
- Then call in a browser (or use curl or links2 in a Terminal session): http://mydomain.com



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

Instead using localhost (127.0.0.1) we will use an own local domain and will setup therefore this domain (and all subdomains too!)
in the /etc/hosts of the machine you call from (if it is the same as where you run your docker-compose.yml you have to do it there too)!
Advantage is, we can call all URL's from any other server then the one we are serving our docker-compose.yml!

Open on the Machine you want to call from (<IP-Address> is the IP of the Server you are running the docker-compose.yml - if it is the same host use 127.0.0.1):
sudo nano /etc/hosts
<IP-Address>     mydomain.com
<IP-Address>     api.mydomain.com
<IP-Address>     fief.mydomain.com

If using Windows you have to change it here (if you have Windows installed in another Folder then 'C:\Windows' replace this part sure):
C:\Windows\System32\drivers\etc\hosts
<IP-Address>     mydomain.com
<IP-Address>     api.mydomain.com
<IP-Address>     fief.mydomain.com

Calls (using curl, links2 from a Terminal or from a Browser if you have a GUI on your Machine):
WEB-Page:                 http://mydomain.com
Traefik-Dashboard:        http://mydomain.com:8080
FastAPI-Docs              http://api.mydomain.com/docs
FIEF:                     http://fief.mydomain.com:8000
FIEF (admin):             http://fief.mydomain.com:8000/admin

------------------------------------

