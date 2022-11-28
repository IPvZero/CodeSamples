"""Basic Import Test"""
import os
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from inventory import DEVICES
from utils import load_vars


def generate_config(device_vars):
    """Generate device config"""
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("config.j2")
    configuration = template.render(device_vars)
    return configuration.splitlines()


def configure_junos(hostname, configuration):
    """Push configuration to Juniper device"""
    with ConnectHandler(
        device_type="juniper",
        host=hostname,
        username=os.environ["MYUSERNAME"],
        password=os.environ["MYPASSWORD"],
        port=22,
    ) as conn:
        result = conn.send_config_set(config_commands=configuration)
    print(result)


def main():
    """Main function"""

    for device in DEVICES:
        groups = device["groups"]
        hostname = device["hostname"]
        device_vars = load_vars(device, groups)
        configuration = generate_config(device_vars)
        configure_junos(hostname, configuration)


main()
