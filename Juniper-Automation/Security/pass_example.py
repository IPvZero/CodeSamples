import getpass
from netmiko import ConnectHandler
from rich import print as rprint

myuser = getpass.getpass(prompt="Enter username: ")
cisco_pass = getpass.getpass()

with ConnectHandler(device_type="juniper", host="192.168.4.101", username=myuser, password=mypass, port=22) as conn:
    result = conn.send_command(command_string="show configuration")
    rprint(result)
