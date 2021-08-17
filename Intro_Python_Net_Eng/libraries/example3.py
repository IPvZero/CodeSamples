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
        response = conn.send_command("show ip interface brief")
    print(response.result)
