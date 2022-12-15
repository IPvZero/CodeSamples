import json
from scrapli import Scrapli
from rich import print as rprint

def connect_junos(device_ip):
    device = {
        "host": device_ip,
        "auth_username": "john",
        "auth_password": "Juniper1",
        "auth_strict_key": False,
        "platform": "juniper_junos",
    }

    conn = Scrapli(**device)
    conn.open()
    result = conn.send_command("show ospf neighbor | display json")
    pretty_result = json.loads(result.result)
    return pretty_result

def parse_ospf(device_ip, pretty_result):
    state = pretty_result["ospf-neighbor-information"]["ospf-neighbor"]["ospf-neighbor-state"]
    if state == "Full":
        return f"OSPF Adjacency is fully established on {device_ip}"
    else:
        return f"OSPF Adjacency is NOT fully established on {device_ip}"


pretty_result = connect_junos("192.168.4.101")
result = parse_ospf("192.168.4.101", pretty_result)
print(result)