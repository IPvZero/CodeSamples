from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from rich import print as rprint
import getpass
import sys

mypass = getpass.getpass()

device = Device(host="192.168.4.101", user="john", passwd=mypass)
try:
    device.open()
except ConnectError as err:
    print("Connection to Device failed")
    sys.exit(1)
except Exception as err:
    print(err)
    sys.exit(1)

response = device.facts
# rprint(response.keys())
print(f"The device hostname is {response['hostname']}")
print(f"The serial numnber is {response['serialnumber']}")
print(f"The version of the device is {response['version']}")
