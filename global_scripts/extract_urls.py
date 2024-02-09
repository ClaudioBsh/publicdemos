import yaml
import re
import socket
import sys

dcfile = ""
if len(sys.argv) > 1:
    dcfile = sys.argv[1]
else:
    dcfile = "docker-compose.yml"
file_path = dcfile
print(f"Using this docker-compose file: {dcfile}")

# Öffnen und Analysieren der docker-compose.yml-Datei
with open(file_path, "r") as file:
    docker_compose = yaml.safe_load(file)

    # Durchsuchen der Services und Extrahieren der Traefik-Host-Regeln
    print(f"{'Service':<30} {'URL':<50}")
    print("-" * 80)
    for service, config in docker_compose.get('services', {}).items():
        if 'labels' in config:
            labels = config['labels']
            for label in labels:
                if label.startswith("traefik.http.routers.") and "rule=Host(" in label:
                    host_rule = re.search(r"Host\(`([^`]+)`\)", label).group(1)
                    for l in labels:
                        if l.startswith("traefik.http.routers." + service + ".rule"):
                            path_prefix_match = re.search(r"PathPrefix\(`([^`]+)`\)", l)
                            path_prefix = path_prefix_match.group(1) if path_prefix_match else ""
                            full_url = f"http://{host_rule}/{path_prefix.lstrip('/')}"
                            print(f"{service:<30} {full_url:<50}")

        # Durchsuchen der Ports unter 'services'
        if 'ports' in config:
            ports = config['ports']
            for port in ports:
                if ':' in port:
                    host_port, container_port = port.split(':')
                else:
                    host_port = port
                full_url = f"http://{socket.gethostbyname(socket.gethostname())}:{host_port}"
                print(f"{service:<30} {full_url:<50}")

    # Durchsuchen der Labels unter 'deploy'
    for service, config in docker_compose.get('services', {}).items():
        if 'deploy' in config and isinstance(config['deploy'], dict) and 'labels' in config['deploy']:
            labels = config['deploy']['labels']
            for label in labels:
                if label.startswith("traefik.http.routers.") and "rule=Host(" in label:
                    host_rule = re.search(r"Host\(`([^`]+)`\)", label).group(1)
                    for l in labels:
                        if l.startswith("traefik.http.routers." + service + ".rule"):
                            path_prefix_match = re.search(r"PathPrefix\(`([^`]+)`\)", l)
                            path_prefix = path_prefix_match.group(1) if path_prefix_match else ""
                            full_url = f"http://{host_rule}/{path_prefix.lstrip('/')}"
                            print(f"{service:<30} {full_url:<50}")
