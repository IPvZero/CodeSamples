import requests

requests.packages.urllib3.disable_warnings()

device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "port": "443",
    "user": "developer",
    "password": "C1sco12345",
}

headers = {"Accept": "application/yang-data+json"}

url = f"https://{device['host']}:{device['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1"

response = requests.get(
    url=url, headers=headers, auth=(device["user"], device["password"]), verify=False
)

response.raise_for_status()
print(response.text)
