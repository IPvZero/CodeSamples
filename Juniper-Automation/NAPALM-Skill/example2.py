from napalm import get_network_driver
from rich import print as rprint

juniper_device = get_network_driver("junos")

with juniper_device(
    hostname="192.168.4.101", username="john", password="Juniper1"
) as device:
    results = device.get_facts()
rprint(results)
