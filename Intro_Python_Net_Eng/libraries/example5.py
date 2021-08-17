import json
from scrapli.driver.core import IOSXEDriver


MY_DEVICES = [
    {
        "host": "192.168.31.101",
        "auth_username": "john",
        "auth_password": "cisco",
        "auth_strict_key": False,
        "ssh_config_file": True,
    },
    {
        "host": "192.168.31.102",
        "auth_username": "john",
        "auth_password": "cisco",
        "auth_strict_key": False,
        "ssh_config_file": True,
    },
    {
        "host": "192.168.31.103",
        "auth_username": "john",
        "auth_password": "cisco",
        "auth_strict_key": False,
        "ssh_config_file": True,
    },
]

for device in MY_DEVICES:
    with IOSXEDriver(**device) as conn:
        response = conn.send_command("show version")
    structured_result = response.textfsm_parse_output()
    for info in structured_result:
        print(f"Device {info['hostname']} has a serial number of {info['serial'][0]}")
        print("\n\n")
        
