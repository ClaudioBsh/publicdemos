#!/bin/bash

cd ..

VARS_FILE="config/jinja_vars.yml"

for template in *.j2; do
    output_file="${template%.j2}"
    jinja2 "$template" "$VARS_FILE" > "$output_file"
done
