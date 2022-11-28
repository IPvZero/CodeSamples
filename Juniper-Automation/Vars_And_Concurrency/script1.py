import yaml
from inventory import DEVICES
from rich import print as rprint


def load_vars(device, groups):
    device_name = device["device_name"]
    data_dict = {}
    host_data = yaml.safe_load(open(f"host_vars/{device_name}.yaml"))
    rprint(host_data)


def main():
    for device in DEVICES:
        groups = device["groups"]
        device_vars = load_vars(device, groups)


main()
