from rich import print as rprint
from napalm import get_network_driver

DEVICES = [
    {
        "hostname": "192.168.31.101",
        "username": "john",
        "password": "cisco",
        "driver": "ios",
    },
    {
        "hostname": "192.168.31.102",
        "username": "john",
        "password": "cisco",
        "driver": "ios",
    },
    {
        "hostname": "192.168.31.103",
        "username": "john",
        "password": "cisco",
        "driver": "ios",
    },
    {
        "hostname": "192.168.31.104",
        "username": "john",
        "password": "Juniper1",
        "driver": "junos",
    },
]

for dev in DEVICES:
    driver = get_network_driver(dev["driver"])
    with driver(
        username=dev["username"], password=dev["password"], hostname=dev["hostname"]
    ) as device:
        result = device.get_facts()
    rprint(
        f"{result['hostname']} is a {result['vendor']} device - serial number {result['serial_number']}"
    )
   
