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

General:
Have in mind that for your Host you running FIEF on, you have to configure your Router/Firewall (protocoll 'tcp')!
It needs to be open on Port 8000 (FIEF Default Port) and optional Port 8080 for using Traefik-Dashboard!
And sure on Ports 80 and 443 for http/https!

URL-Calls (using curl, links2 from a Terminal or from a Browser if you have a GUI on your Machine) localhost:
WEB-Page:                 http://localhost
Traefik-Dashboard:        http://localhost:8080
NiceGUI                   http://api.localhost
FastAPI-Docs              http://api.localhost/docs
FIEF (login):             http://fiefdemo.localhost:8000/login
FIEF (admin):             http://fiefdemo.localhost:8000/admin

URL-Calls (using curl, links2 from a Terminal or from a Browser if you have a GUI on your Machine) with a real ssl/tls domain:
WEB-Page:                 https://yourdomain.xx
Traefik-Dashboard:        https://yourdomain.xx:8080
NiceGUI                   https://api.yourdomain.xx
FastAPI-Docs              https://api.yourdomain.xx/docs
FIEF (login):             https://fiefdemo.yourdomain.xx/login
FIEF (admin):             https://fiefdemo.yourdomain.xx/admin

IP-Calls (using curl, links2 from a Terminal or from a any other Browser which is available to call your machine running the FIEFDEMO):
WEB-Page:                 http://<IP>
Traefik-Dashboard:        http://<IP>:8080
NiceGUI                   http://<IP>:8001
FastAPI-Docs              http://<IP>:8001/docs
FIEF (login):             http://<IP>:8000/login
FIEF (admin):             http://<IP>:8000/admin => will not work with FIEF-Server 0.27.0, because the need of using 'localhost' or a real domain (ssl/tls - https)!
                          Think about using 'ngrok' - more details you can find here: https://github.com/orgs/fief-dev/discussions/37

------------------------------------

If you use Raspbian (Raspberry) instead Ubuntu/Debian and get in trouble with missing Python-Packages when running 'run.sh':

Be sure you have Python3 with PIP3 installed!

Iy yes, then open a terminal and call these commands:
sudo apt install python3-venv python3-pip
cd <root_of_your_sourcecode_folder>
python3 -m venv venv
source venv/bin/activate
pip install Jinja2
pip install PyYaml

Now you should be able to use 'run.sh' on Raspbian too.

------------------------------------

Router / Firewall:

Please make sure, that in case you use an external Domain that on the environment of the FIEF-Host
you have to give the following Ports open (protocoll is 'tcp'):
80	=> http
443	=> https
8000	=> FIEF
8080	=> Traefik-Dashboard (This is optional, only needed, if you want to access Traefik-Dashboard on PORT 8080)

------------------------------------

"Http Code 526" in case you use a public domain which you are the owner from:

Guess you use a DNS provider like e.g. Cloudflare and you did change from http to https or vice versa,
then you have temporary to deactivate "proxied" mode on your DNS-Provider-URL-Page for the domain (and for each subdomain too!!) you use,
wait at least about 5min (sometimes more, but should not more then 20min), then test url access again.
You could additionaly purge the cache - find it within your DNS-Provider-Account!

After the wait time is over and access was working again, you can switch back to "proxied" mode.

If it is still not working, you have to check your Traefik-Service configuration and your DNS-Provider configuration at all!

See more:

https://developers.cloudflare.com/ssl/troubleshooting/general-ssl-errors/
Have in mind - Cloudflare free account supports only:
subdomain.domain.com
It does not support:
sub.subdomain.domain.com
For using this, you need to pay Cloudflare!

https://community.cloudflare.com/t/ssl-error-526-out-of-a-sudden-lets-encrypt-cert-still-valid-for-59-days-and-no-changes/433395/4
It could help to change "SSL/TLS" from "Full (strict)" to "Full" (this affect you can test fast, you have normaly not to wait)
and/or pause your Cloudflare, try the access to your domain, if it is accessible again, unpause Cloudflare.

------------------------------------

Error (FIEF Server logs) "invalid_grant":

This error can have many different problems as shown here:
https://blog.timekit.io/google-oauth-invalid-grant-nightmare-and-how-to-fix-it-9f4efaf1da35#.eqa5iwbkt
Short description: 
RFC 6749 OAuth 2.0 defined invalid_grant as: 
The provided authorization grant (e.g., authorization code, resource owner credentials)
or refresh token is invalid, expired, revoked, does not match the redirection URI used
in the authorization request, or was issued to another client.

Try this so solve any error around "invalid_grant":

First of all make sure tls/acme is working fine!
If you unproxied get error unsecure website but acme.json is created,
then it seems traefik does not handle ssl/tls correctly!
This warning will not pop up when letsencrypt, acme and traefik are working fine together!
Make sure:
- acme.json has permission 600
- Owner/Group is same as the user who is starting containers (should not be user root)
- Do not use letsencrypt staging server
- Delete any cookie from you Browser regarding FIEF

When you change your DNS settings e.g. within Cloudflare, think on to do these steps:
- stop all containers 
- remove acme.json
- dns unproxy domain and all subdomains 
- dns ssl/tls to full strict 
- dns cache config purge all 
- wait 5-20min 
- start containers 
- wait 1min so letsencrypt can create whole acme.json 
- test fiefdemo..../admin 
- if it is working now, fine, change dns to proxied
- dns cache config purge all 
- stop all containers 
- remove acme.json 
- wait 5-20min 
- start containers 
- wait 1min so letsencrypt can create whole acme.json
- test fiefdemo..../admin
- should be fine

When testing change DNS Caching Browser-Cache-TTL to 2min
For prod much higher, e.g. 4h or 1 day

------------------------------------

With FIEF 0.28.5 (and lower) SSL/TLS with real domain got not running fine, the "/admin" path does not work successfull:

The FIEF Author is working on this issue: https://github.com/orgs/fief-dev/discussions/347 and https://github.com/fief-dev/fief/issues/349

As a workaround use FIEF as http only and not using Traefik, use Traefik for https only services.

So current version of this Demo is using this workaround!

------------------------------------
