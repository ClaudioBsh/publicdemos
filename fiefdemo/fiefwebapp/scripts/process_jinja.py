# process_jinja.py
import sys
from jinja2 import Environment, FileSystemLoader
import yaml

# First Argument is the path to the template, second to the variables file
template_path, vars_file = sys.argv[1], sys.argv[2]

# Load from variables file
with open(vars_file, 'r') as file:
    variables = yaml.safe_load(file)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(template_path)
rendered_content = template.render(variables)
print(rendered_content)
