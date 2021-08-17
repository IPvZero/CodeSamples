from scrapli.driver.core import IOSXEDriver

MY_DEVICE = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
}

with IOSXEDriver(**MY_DEVICE) as conn:
    response = conn.send_configs_from_file("config.txt")
print(response.result)
