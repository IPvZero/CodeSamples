from netmiko import ConnectHandler
from rich import print as rprint
from inventory import DEVICES

def configure_device(hostname):
    with ConnectHandler(device_type="juniper", host=hostname, username="john", password="Juniper1", port=22) as conn:
        conn.send_command(command_string="request system configuration rescue save")

def main():
    for device in DEVICES:
        hostname = device["hostname"]
        configure_device(hostname)

main()


