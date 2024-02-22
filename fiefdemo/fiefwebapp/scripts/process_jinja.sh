#!/bin/bash

cd ..

VARS_FILE="config/jinja_vars.yml"

find . -name '*.j2' | while read template; do
    clean_template=${template#./}
    output_file="${clean_template%.j2}"
    python scripts/process_jinja.py "$clean_template" "$VARS_FILE" > "$output_file"
done
