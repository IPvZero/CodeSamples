from napalm import get_network_driver
from rich import print as rprint

juniper_device = get_network_driver("junos")

my_device = juniper_device(
    hostname="192.168.4.101", username="john", password="Juniper1"
)
my_device.open()
results = my_device.get_users()
rprint(results)
my_device.close()
