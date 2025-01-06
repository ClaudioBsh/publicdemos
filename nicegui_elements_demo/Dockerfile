# Nutze das Python Base-Image (armv7 für Raspberry Pi)
FROM python:3.10-slim

# Installiere System-Abhängigkeiten (falls nötig, z. B. für NiceGUI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere den App-Code in das Arbeitsverzeichnis
COPY . /app

# Installiere Python-Bibliotheken (z. B. NiceGUI)
#RUN pip install --no-cache-dir nicegui
RUN pip install nicegui

# Starte die NiceGUI-App
CMD ["python", "main.py"]
