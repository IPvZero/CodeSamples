import os
from netmiko import ConnectHandler
from rich import print as rprint

myuser = os.environ["MYUSERNAME"]
mypass = os.environ["MYPASSWORD"]

with ConnectHandler(device_type="juniper", host="192.168.4.101", username=myuser, password=mypass, port=22) as conn:
    result = conn.send_command(command_string="show configuration")
    rprint(result)
