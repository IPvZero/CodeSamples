""" Multivendor Parsing Example """
from napalm import get_network_driver
from rich import print as rprint
from inventory import DEVICES


def connect_cisco(hostname, username, password):
    """Function to Connect to Cisco platforms"""

    cisco_device = get_network_driver("ios")
    with cisco_device(hostname=hostname, username=username, password=password) as conn:
        result = conn.get_facts()
    getter_parser_printer(result)


def connect_juniper(hostname, username, password):
    """Function to Connect to Juniper platforms"""

    juniper_device = get_network_driver("junos")
    with juniper_device(
        hostname=hostname, username=username, password=password
    ) as conn:
        result = conn.get_facts()
    getter_parser_printer(result)


def getter_parser_printer(result):
    """Function to parse and print each result"""

    hostname = result["hostname"]
    serial_number = result["serial_number"]
    vendor = result["vendor"]
    uptime = result["uptime"]
    rprint(f"{hostname} ({serial_number}/{vendor}) has an uptime of {uptime}")


def main():
    """Main execution point"""

    for device in DEVICES:
        hostname = device["hostname"]
        username = device["username"]
        password = device["password"]
        platform = device["platform"]
        if platform == "cisco":
            connect_cisco(hostname, username, password)
        elif platform == "juniper":
            connect_juniper(hostname, username, password)
        else:
            print("Sorry, please select 'cisco' or ' juniper' for the platform")


main()
