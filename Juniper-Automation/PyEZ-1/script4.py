import sys
import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from rich import print as rprint
from lxml import etree
import xmltodict

mypass = getpass.getpass()

device = Device(host="192.168.4.101", user="john", passwd=mypass)
try:
    device.open()
except ConnectError as err:
    print("Device connection failed")
    sys.exit(1)
except Exception as err:
    print(err)
    sys.exit(1)

response = device.rpc.get_ospf_overview_information()
rprint(etree.tostring(response, pretty_print=True).decode())
ospf_router_id = response.find(".//ospf-router-id").text
ospf_area = response.find(".//ospf-area").text
print(f"The ospf area is {ospf_area} and the OSPF router_id is {ospf_router_id}")
