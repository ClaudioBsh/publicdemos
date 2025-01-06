#!/usr/bin/env python3

#Wenn der Dateiname mit Ordner übergeben wird:
#python show_code_gpt_optimized.py meinordnername/meindatei
#Der Ordner meinordnername wird als Startpunkt verwendet, und ab dort wird rekursiv nach meindatei gesucht.

#Wenn nur der Dateiname ohne Ordner übergeben wird:
#python show_code_gpt_optimized.py meindatei
#Die Suche startet im aktuellen Verzeichnis und geht rekursiv in alle Unterverzeichnisse.

import sys
import os

def find_file(start_path, filename):
    """
    Sucht rekursiv in einem Startpfad (start_path) nach einer Datei (filename).
    """
    for root, dirs, files in os.walk(start_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def clean_file(file_path):
    """
    Öffnet und verarbeitet die Datei (Dateien werden aufbereitet und Kommentare entfernt).
    """
    try:
        # Lese zuerst die gesamte Datei
        with open(file_path, 'r') as file:
            content = file.read()

        # Entferne Markdown-Kommentare zwischen """ und """
        while '"""' in content:
            start = content.find('"""')
            end = content.find('"""', start + 3)
            if end == -1:  # Falls kein schließendes """ gefunden wird
                break
            content = content[:start] + content[end + 3:]

        # Verarbeite den bereinigten Inhalt zeilenweise
        for line in content.splitlines():
            # Überspringe leere Zeilen oder Zeilen nur mit Whitespace
            if line.strip() == '':
                continue

            # Überspringe Zeilen, die mit # beginnen
            if line.strip().startswith('#'):
                continue

            # Suche nach #, die nicht in Anführungszeichen sind
            new_line = ''
            in_single_quote = False
            in_double_quote = False

            for i, char in enumerate(line):
                if char == "'" and (i == 0 or line[i-1] != '\\'):
                    in_single_quote = not in_single_quote
                elif char == '"' and (i == 0 or line[i-1] != '\\'):
                    in_double_quote = not in_double_quote
                elif char == '#' and not in_single_quote and not in_double_quote:
                    break
                new_line += char

            # Ausgabe nur wenn die Zeile nach der Bereinigung nicht leer ist
            if new_line.strip():
                print(new_line.rstrip())

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <foldername/filename>", file=sys.stderr)
        sys.exit(1)

    # Extrahiere Argument: Pfad zum Ordner/Datei
    argument = sys.argv[1]
    folder, filename = os.path.split(argument)

    # Bestimme den Startpfad für die Suche
    if folder:  # Falls ein Ordner im Argument spezifiziert ist
        start_path = folder
    else:  # Standardmäßig im aktuellen Verzeichnis starten
        start_path = '.'

    # Suche die Datei
    file_path = find_file(start_path, filename)

    if file_path is None:
        print(f"Error: File '{filename}' not found starting from '{start_path}'", file=sys.stderr)
        sys.exit(1)

    # Bereinige die gefundene Datei
    clean_file(file_path)
