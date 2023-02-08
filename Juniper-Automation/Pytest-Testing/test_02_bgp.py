import json
import pytest
from netmiko import ConnectHandler


def get_devices():
    devices = ["192.168.4.101", "192.168.4.102"]
    return devices


@pytest.mark.parametrize("device", get_devices())
def test_bgp_peer(device):
    conn = ConnectHandler(
        device_type="juniper_junos",
        ip=device,
        username="john",
        password="Juniper1",
    )
    result = conn.send_command(command_string="show bgp summary | display json")
    dict_result = json.loads(result)
    state = dict_result["bgp-information"]["bgp-peer"]["peer-state"]
    assert state == "Established"
