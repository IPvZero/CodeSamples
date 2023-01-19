import yaml
from jinja2 import Environment, FileSystemLoader
from ncclient import manager
from inventory import DEVICES


def generate_configs(device_name):
    yaml_data = yaml.safe_load(open(f"host_vars/{device_name}.yaml"))
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("ospf.j2")
    configuration = template.render(yaml_data)
    return configuration


def configure_device(hostname, username, password, configuration):
    with manager.connect(
        host=hostname,
        port="830",
        timeout=30,
        username=username,
        password=password,
        device_params={"name": "junos"},
        hostkey_verify=False,
    ) as m:
        response = m.rpc(configuration)
        print(response)


def main():
    for device in DEVICES:
        device_name = device["device_name"]
        hostname = device["hostname"]
        username = device["username"]
        password = device["password"]
        configuration = generate_configs(device_name)
        configure_device(hostname, username, password, configuration)


main()
