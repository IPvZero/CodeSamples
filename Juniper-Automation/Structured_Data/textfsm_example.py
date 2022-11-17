""" Netmiko TextFSM Example"""
from netmiko import ConnectHandler
from rich import print as rprint

my_device = {
    "device_type": "juniper_junos",
    "host": "192.168.4.101",
    "username": "john",
    "password": "Juniper1",
    "port": 22,
}

with ConnectHandler(**my_device) as conn:
    result = conn.send_command(command_string="show interfaces", use_textfsm=True)
rprint(result)
