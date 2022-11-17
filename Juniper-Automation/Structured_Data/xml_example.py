"""Simple XML Example"""
from netmiko import ConnectHandler
import xmltodict
from rich import print as rprint

my_device = {
    "device_type": "juniper",
    "host": "192.168.4.101",
    "username": "john",
    "password": "Juniper1",
    "port": 22,
}

with ConnectHandler(**my_device) as conn:
    result = conn.send_command(command_string="show interfaces terse | display xml")
    dict_result = xmltodict.parse(result)
phys_result = dict_result["rpc-reply"]["interface-information"]["physical-interface"]
for x in phys_result:
    rprint(x["admin-status"])
