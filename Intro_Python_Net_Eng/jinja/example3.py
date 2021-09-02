import yaml
from jinja2 import Environment, FileSystemLoader

def generate_config():
    """
    Load in host variables.
    Generate config from template
    """
    my_vars = yaml.safe_load(open("R1.yaml"))
    env = Environment(loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("snmp.j2")
    configuration = template.render(my_vars)
    print(configuration)

generate_config()
