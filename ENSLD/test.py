"""
Before running this script be sure to pip install the following libraries:

python3 -m pip install scrapli-netconf
python3 -m pip install rich

"""

from scrapli_netconf.driver import NetconfScrape
from rich import print as rprint

device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
    "port": 830
}

connection = NetconfScrape(**device)
connection.open()
output = connection.server_capabilities
rprint(output)
