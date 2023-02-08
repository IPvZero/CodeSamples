import json
from netmiko import ConnectHandler


def test_bgp_peer():
    conn = ConnectHandler(
        device_type="juniper_junos",
        ip="192.168.4.101",
        username="john",
        password="Juniper1",
    )
    result = conn.send_command(command_string="show bgp summary | display json")
    dict_result = json.loads(result)
    state = dict_result["bgp-information"]["bgp-peer"]["peer-state"]
    assert state == "Active"
