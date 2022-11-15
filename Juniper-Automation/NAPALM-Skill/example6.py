from napalm import get_network_driver
from rich import print as rprint
import yaml

juniper_device = get_network_driver("junos")

with juniper_device(
    hostname="192.168.4.101", username="john", password="Juniper1"
) as device:
    results = device.get_facts()
    yaml_result = yaml.safe_dump(results)
rprint(yaml_result)
