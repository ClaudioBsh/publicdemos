#!/bin/bash

# Tipp for start with log on terminal and to a logfile:
# ./container_run_logs.sh 2>&1 | tee ./container_run_logs.log
# ./container_run_logs.sh 2>&1 | tee ../tmp/log/container_run_logs.log

# Aufruf ohne Parameter untersucht ALLE laufenden Container und gibt per Default die letzten 3 Logzeilen aus
# Man kann als 1. Parameter einfach einen anderen Wert als 3 angeben, dann wird wird diese Anzahl an letzten Logzeilen ausgegeben

# Aufruf mit einem Containernamen (ermittle den Namen mit z.B.: docker ps), dann wird NUR dieser eine Container untersucht
# ./container_run_logs.sh 15 containername

# Aufruf mit einer Datei die eine Liste (pro Zeile eine!) mit Containernamen enthaelt, untersucht dann NUR alle diese Container laut dieser Liste!
# ./container_run_logs.sh 20 $(cat container_list.txt)

# clear

# Funktion zum Anzeigen der letzten N Zeilen der Logs für einen Container
show_container_logs() {
  local container_name=$1
  local num_lines=${2:-${defaultnumoflogline}}

  echo ""
  echo "----------------------------------------"
  echo "Last $num_lines lines of logs for container: $container_name"
  echo "----------------------------------------"
  docker logs --tail $num_lines $container_name
  echo "----------------------------------------"
  echo ""
}

# Funktion zum Verarbeiten aller Container
process_containers_logs() {
  local container_list=$1
  local num_lines=$2

  # Schleife über alle Container
  for container in $container_list; do
    show_container_logs "$container" "$num_lines"
  done
}

get_container_list() {
  if [ "$#" -eq 1 ] && [ -f "$1" ]; then
    cat "$1"
  else
    docker ps --format '{{.Names}}'
  fi
}

# Setze die Standardanzahl der Logzeilen
defaultnumofloglines=3

# Überprüfe die Anzahl der Parameter
if [ "$#" -eq 0 ]; then
  # Ohne Parameter, verarbeite alle laufenden Container
  num_lines=$defaultnumofloglines
  container_list=$(get_container_list)
elif [ "$#" -eq 1 ] && [ "$1" -eq "$1" ] 2>/dev/null; then
  # Ein Parameter als Zahl, passe die Anzahl der Logzeilen an
  num_lines=$1
  container_list=$(get_container_list)
elif [ "$#" -eq 1 ] && [ -f "$1" ]; then
  # Ein Parameter als Datei, verarbeite die Einträge als Container
  num_lines=$defaultnumofloglines
  container_list=$(get_container_list "$1")
elif [ "$#" -eq 2 ] && [ "$1" -eq "$1" ] 2>/dev/null && [ ! -f "$2" ]; then
  # Zwei Parameter: Zahl für Logzeilen und Container als Text
  num_lines=$1
  container_list="$2"
elif [ "$#" -eq 2 ] && [ "$1" -eq "$1" ] 2>/dev/null && [ -f "$2" ]; then
  # Zwei Parameter: Zahl für Logzeilen und Datei mit Containernamen
  num_lines=$1
  container_list=$(get_container_list "$2")
else
  # Andernfalls, zeige eine Meldung zur Verwendung des Skripts
  echo "Verwendung: $0 [ANZAHL_LOGZEILEN] [CONTAINER_DATEI]"
  exit 1
fi

process_containers_logs "$container_list" "$num_lines"

