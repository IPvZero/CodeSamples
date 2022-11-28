import yaml
import os
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler


def load_vars(device, groups):
    device_name = device["device_name"]
    data_dict = {}
    default_data = yaml.safe_load(open("group_vars/defaults.yaml"))
    if default_data is not None:
        for k, v in default_data.items():
            data_dict[k] = v
    all_group_data = []
    for group in groups:
        group_data = yaml.safe_load(open(f"group_vars/{group}.yaml"))
        if group_data is not None:
            all_group_data.append(group_data)
    for group_data in all_group_data:
        for k, v in group_data.items():
            data_dict[k] = v
    host_data = yaml.safe_load(open(f"host_vars/{device_name}.yaml"))
    if host_data is not None:
        for k, v in host_data.items():
            data_dict[k] = v
    return data_dict


def generate_config(device_vars):
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("config.j2")
    configuration = template.render(device_vars)
    return configuration.splitlines()


def configure_junos(hostname, configuration):
    with ConnectHandler(
        device_type="juniper",
        host=hostname,
        username=os.environ["MYUSERNAME"],
        password=os.environ["MYPASSWORD"],
        port=22,
    ) as conn:
        result = conn.send_config_set(config_commands=configuration)
    print(result)
