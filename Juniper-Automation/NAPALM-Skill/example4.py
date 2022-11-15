from napalm import get_network_driver
from rich import print as rprint

juniper_device = get_network_driver("junos")

with juniper_device(
    hostname="192.168.4.101", username="john", password="Juniper1"
) as device:
    device.load_replace_candidate(filename="R1.cfg")
    compare_result = device.compare_config()
    rprint(compare_result)
    answer = input("Do you want to commit this configuration? <y/n> ")
    if answer == "y":
        device.commit_config()
        print("Configuration Committed.")
    else:
        device.discard_config()
        print("Configuration Discarded.")
