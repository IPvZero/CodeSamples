import pytest
from scrapli.driver.core import IOSXEDriver
from inv import DEVICES


@pytest.mark.parametrize("device", DEVICES)
def test_number_interfaces(device):
    with IOSXEDriver(
        host=device["host"],
        auth_username="john",
        auth_password="cisco",
        auth_strict_key=False,
        ssh_config_file=True,
    ) as conn:
        response = conn.send_command("show interfaces")
    structured_result = response.textfsm_parse_output()
    assert len(structured_result) == 4
