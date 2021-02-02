"""

Before running this script you must pip install the Scrapli-Netconf library:
python3 -m pip install scrapli-netconf

"""
from scrapli_netconf.driver import NetconfScrape

device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
    "port": 830,
}


myfilter = """
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
  </interfaces>
"""

connection = NetconfScrape(**device)
connection.open()
response = connection.get(filter_=myfilter, filter_type="subtree")
print(response.result)
