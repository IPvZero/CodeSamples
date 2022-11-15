from napalm import get_network_driver
from rich import print as rprint
import yaml

juniper_device = get_network_driver("junos")

with juniper_device(
    hostname="192.168.4.101", username="john", password="Juniper1"
) as device:
    results = device.compliance_report("R1-validate.yaml")
if results["get_facts"]["complies"] == True:
    rprint("R1 is compliant")
else:
    rprint("R1 is not compliant")
