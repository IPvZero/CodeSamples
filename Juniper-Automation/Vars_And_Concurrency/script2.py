import yaml
from inventory import DEVICES
from rich import print as rprint


def load_vars(device, groups):
    device_name = device["device_name"]
    data_dict = {}
    host_data = yaml.safe_load(open(f"host_vars/{device_name}.yaml"))
    if host_data is not None:
        for k, v in host_data.items():
            data_dict[k] = v
    all_group_data = []
    for group in groups:
        group_data = yaml.safe_load(open(f"group_vars/{group}.yaml"))
        if group_data is not None:
            all_group_data.append(group_data)
    for group_data in all_group_data:
        for k, v in group_data.items():
            data_dict[k] = v
    rprint(data_dict)
    print("\n\n")


def main():
    for device in DEVICES:
        groups = device["groups"]
        device_vars = load_vars(device, groups)


main()
