import json
import pytest
from netmiko import ConnectHandler

test_map = {"192.168.4.101": "R1", "192.168.4.102": "R2"}


def get_devices():
    devices = ["192.168.4.101", "192.168.4.102"]
    return devices


@pytest.mark.parametrize("device", get_devices())
def test_hostname(device):
    conn = ConnectHandler(
        device_type="juniper_junos",
        ip=device,
        username="john",
        password="Juniper1",
    )
    result = conn.send_command(
        command_string="show configuration system host-name | display json"
    )
    dict_result = json.loads(result)
    name = dict_result["configuration"]["system"]["host-name"]
    expected_name = test_map[device]
    assert name == expected_name
