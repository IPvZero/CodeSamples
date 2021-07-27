from scrapli.driver.core import IOSXEDriver

MY_DICT = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
}

with IOSXEDriver(**MY_DICT) as conn:
    result = conn.send_command("show version")

print(result.result)
