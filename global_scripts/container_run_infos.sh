#!/bin/bash

# Tipp for start with log on terminal and to a logfile:
# ./container_run_infos.sh 2>&1 | tee ./container_run_infos.log
# ./container_run_infos.sh 2>&1 | tee ../tmp/log/container_run_infos.log

# Aufruf ohne Parameter untersucht ALLE laufenden Container

# Aufruf mit einem Containernamen (ermittle den Namen mit z.B.: docker ps), dann wird NUR dieser eine Container untersucht
# ./container_run_infos.sh containername

# Aufruf mit einer Datei die eine Liste (pro Zeile eine!) mit Containernamen enthaelt, untersucht dann NUR alle diese Container laut dieser Liste!
# ./container_run_infos.sh container_list.txt

# clear

print_container_service_name() {
  local container_name=$1
  local container_service_name=$(docker inspect -f '{{index .Config.Labels "com.docker.compose.service"}}' $container_name)

  printf "%-30s | %-30s" "$container_name" "$container_service_name"
}

print_container_networks() {
  local container_name=$1
  local container_networks=$(docker inspect -f '{{range $key, $value :=.NetworkSettings.Networks}}{{printf "%s;%s\n" $key $value.Gateway}}{{end}}' $container_name)

  # Überprüfe, ob Networks vorhanden sind, um %!s(MISSING) zu vermeiden
  if [ -n "$container_networks" ]; then
    # Schleife über alle Networks für formatierte Ausgabe
    printf "%-30s | %-40s | %-20s\n" "$container_name" "" ""
    while IFS=';' read -r network gateway; do
      printf "%-30s | %-40s | %-20s\n" "" "$network" "$gateway"
    done <<< "$container_networks"
  else
    printf "%-30s | %-40s | %-20s\n" "$container_name" "No Networks" "No Gateway"
  fi
}


print_container_ip_addresses() {
  local container_name=$1
  local container_ip_networks=$(docker inspect --format='{{range $key, $value := .NetworkSettings.Networks}}{{.IPAddress}};{{.NetworkID}}{{printf "\n"}}{{end}}' $container_name)

  if [ -n "$container_ip_networks" ]; then
    printf "%-30s | %-20s | %-20s\n" "$container_name" "" ""
    while IFS=';' read -r ip_address network_id; do
      network_name=$(docker network inspect -f '{{.Name}}' $network_id)
      printf "%-30s | %-20s | %-20s\n" "" "$ip_address" "$network_name"
    done <<< "$container_ip_networks"
  else
    printf "%-30s | %-20s | %-30s\n" "$container_name" "No IP Addresses" "No Networks"
  fi
}


print_container_ports() {
  local container_name=$1
  local container_ports=$(docker port $container_name | awk '{printf "%s -> %s\n", $3, $1}')

  if [ -n "$container_ports" ]; then
    printf "%-30s | %-40s\n" "$container_name" ""
    while IFS= read -r port; do
      printf "%-30s | %-40s\n" "" "$port"
    done <<< "$container_ports"
  else
    printf "%-30s | %-40s\n" "$container_name" "No Ports"
  fi
}

print_container_exposed_ports() {
  local container_name=$1
  local container_exposed_ports=$(docker inspect --format='{{range $key, $value := .Config.ExposedPorts}}{{printf "%s\n" $key}}{{end}}' $container_name)

  if [ -n "$container_exposed_ports" ]; then
    printf "%-30s | %-40s\n" "$container_name" ""
    while IFS= read -r port; do
      printf "%-30s | %-40s\n" "" "$port"
    done <<< "$container_exposed_ports"
  else
    printf "%-30s | %-40s\n" "$container_name" "No Exposed Ports"
  fi
}

print_container_volumes() {
  local container_name=$1
  local container_volumes=$(docker inspect -f '{{range .Mounts}}{{.Source}}{{printf "\n"}}{{end}}' $container_name)

  # Überprüfe, ob Mounts vorhanden sind, um %!s(MISSING) zu vermeiden
  if [ -n "$container_volumes" ]; then
    # Schleife über alle Volumes für formatierte Ausgabe
    printf "%-30s | %-90s\n" "$container_name" ""
    while IFS= read -r volume; do
      printf "%-30s | %-90s\n" "" "$volume"
    done <<< "$container_volumes"
  else
    printf "%-30s | %-90s\n" "$container_name" "No Volumes"
  fi
}

print_container_environment() {
  local container_name=$1
  local container_environment=$(docker inspect -f '{{range $key, $value := .Config.Env}}{{printf "%s; %s\n" $key $value}}{{end}}' $container_name)

  # Überprüfe, ob Environment vorhanden ist, um %!s(MISSING) zu vermeiden
  if [ -n "$container_environment" ]; then
    # Schleife über alle Environment-Variablen für formatierte Ausgabe
    printf "%-30s | %-90s\n" "$container_name" ""
    while IFS=';' read -r key value; do
      printf "%-30s | %-90s\n" "" "$value"
    done <<< "$container_environment"
  else
    printf "%-30s | %-90s\n" "$container_name" "No Environment"
  fi
}

print_container_labels() {
  local container_name=$1
  local container_labels=$(docker inspect -f '{{range $key, $value := .Config.Labels}}{{printf "%s; %s\n" $key $value}}{{end}}' $container_name)

  # Überprüfe, ob Labels vorhanden sind, um %!s(MISSING) zu vermeiden
  if [ -n "$container_labels" ]; then
    # Schleife über alle Labels für formatierte Ausgabe
    printf "%-30s | %-45s | %-45s\n" "$container_name" "" ""
    while IFS=';' read -r key value; do
      printf "%-30s | %-45s | %-45s\n" "" "$key" "$value"
    done <<< "$container_labels"
  else
    printf "%-30s | %-45s | %-45s\n" "$container_name" "No Label" "No Value"
  fi
}

print_traefik_labels() {
  local container_name=$1
  local container_labels=$(docker inspect -f '{{range $key, $value := .Config.Labels}}{{if and (eq (printf "%.8s" $key) "traefik.") (ne $key "traefik.enable")}}{{printf "key   => %s\nvalue => %s\n" $key $value}}{{end}}{{end}}' $container_name)

  # Überprüfe, ob Labels vorhanden sind, um %!s(MISSING) zu vermeiden
  if [ -n "$container_labels" ]; then
    # Schleife über alle Labels für formatierte Ausgabe
    printf "%-30s\n" "$container_name"
    while IFS= read -r label; do
      printf "%-30s | %-83s\n" "" "$label"
#      printf "%-30s | %-83s\n" "$container_name" "$label"
    done <<< "$container_labels"
  else
    printf "%-30s | %-83s\n" "$container_name" "No Traefik Label"
  fi
}


# Liste aller Container aus der Datei oder aus den laufenden Containern
get_container_list() {
  if [ "$#" -eq 1 ] && [ -f "$1" ]; then
    cat "$1"
  elif [ "$#" -eq 1 ]; then
    echo "$1"
  else
    docker ps --format '{{.Names}}'
  fi
}

process_containers() {
  local container_list=$1


  ##### REIHENFOLGE DER AUSGABEN ENTSPRECHEND DER NACHFOLGENDEN UEBERSCHRIFTEN UND FOR-SCHLEIFEN #####


  # Überschriften
  echo ""
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"
  printf "%-30s | %-30s\n" "Container Name" "Service Name"
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"

  # Schleife über alle Container für Service Name
  for container in $container_list; do
    echo ""
    print_container_service_name "$container"
  done

  # Überschriften
  echo ""
  echo ""
  echo ""
  printf "%-30s | %-40s | %-20s\n" "------------------------------" "----------------------------------------" "--------------------"
  printf "%-30s | %-40s | %-20s\n" "Container Name" "Network(s)" "Gateway(s)"
  printf "%-30s | %-40s | %-20s\n" "------------------------------" "----------------------------------------" "--------------------"


  # Schleife über alle Container für Netzwerke
  for container in $container_list; do
    echo ""
    print_container_networks "$container"
  done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-20s | %-30s\n" "------------------------------" "--------------------" "------------------------------"
  printf "\n%-30s | %-20s | %-30s\n" "Container Name" "Container IP(s)" "Network(s)"
  printf "%-30s | %-20s | %-30s\n" "------------------------------" "--------------------" "------------------------------"

  # Schleife über alle Container für IP-Adressen
  for container in $container_list; do
    # Füge eine Leerzeile vor jedem Container ein
    echo ""
    print_container_ip_addresses "$container"
  done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"
  printf "%-30s | %-40s\n" "Container Name" "External (open) Port(s)"
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"

  # Schleife über alle Container für Ports
  for container in $container_list; do
    echo ""
    print_container_ports "$container"
  done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"
  printf "%-30s | %-40s\n" "Container Name" "Exposed (internal) Ports"
  printf "%-30s | %-40s\n" "------------------------------" "----------------------------------------"

  # Schleife über alle Container für Exposed Ports
  for container in $container_list; do
    # Füge eine Leerzeile vor jedem Container ein
    echo ""
    print_container_exposed_ports "$container"
  done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-90s\n" "------------------------------" "--------------------------------------------------------------------------------"
  printf "%-30s | %-90s\n" "Container Name" "Container Volumes"
  printf "%-30s | %-90s\n" "------------------------------" "--------------------------------------------------------------------------------"

  # Schleife über alle Container für Volumes
  for container in $container_list; do
    echo ""
    print_container_volumes "$container"
  done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-90s\n" "------------------------------" "--------------------------------------------------------------------------------"
  printf "%-30s | %-90s\n" "Container Name" "Environment entries"
  printf "%-30s | %-90s\n" "------------------------------" "--------------------------------------------------------------------------------"

  # Schleife über alle Container für Environment
  for container in $container_list; do
    echo ""
    print_container_environment "$container"
  done

  ## Überschriften
  #echo ""
  #echo ""
  #printf "%-30s | %-45s | %-45s\n" "------------------------------" "---------------------------------------------" "---------------------------------------------"
  #printf "%-30s | %-45s | %-45s\n" "Container Name" "Label" "Value"
  #printf "%-30s | %-45s | %-45s\n" "------------------------------" "---------------------------------------------" "---------------------------------------------"
  #
  #
  ## Schleife über alle Container für Labels
  #for container in $container_list; do
  #  echo ""
  #  print_container_labels "$container"
  #done

  # Überschriften
  echo ""
  echo ""
  printf "%-30s | %-83s\n" "------------------------------" "---------------------------------------------------------------------------------------"
  printf "%-30s | %-83s\n" "Container Name" "Traefik-Label (key/value)"
  printf "%-30s | %-83s\n" "------------------------------" "---------------------------------------------------------------------------------------"

  # Schleife über alle Container für Labels
  for container in $container_list; do
    echo ""
    print_traefik_labels "$container"
  done
}

# Überprüfe die Anzahl der Parameter
if [ "$#" -eq 0 ]; then
  # Ohne Parameter, verarbeite alle laufenden Container
  container_list=$(get_container_list)
elif [ "$#" -eq 1 ]; then
  # Ein Parameter als Containername oder Datei, verarbeite den/die Eintrag/Einträge als Container
  container_list=$(get_container_list "$1")
else
  # Andernfalls, zeige eine Meldung zur Verwendung des Skripts
  echo "Verwendung: $0 [CONTAINER_DATEI]"
  exit 1
fi

process_containers "$container_list"
