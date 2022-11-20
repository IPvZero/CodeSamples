import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from rich import print as rprint
from inventory import DEVICES


def generate_config(device_name):
    yaml_data = yaml.safe_load(open(f"host_vars/{device_name}.yaml"))
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("config.j2")
    configuration = template.render(yaml_data)
    return configuration.splitlines()


def configure_device(hostname, configuration):
    with ConnectHandler(
        device_type="juniper",
        host=hostname,
        username="john",
        password="Juniper1",
        port=22,
    ) as conn:
        result = conn.send_config_set(config_commands=configuration)
        print(result)


def main():
    for device in DEVICES:
        device_name = device["device_name"]
        hostname = device["hostname"]
        configuration = generate_config(device_name)
        configure_device(hostname, configuration)


main()
