from scrapli.driver.core import IOSXEDriver

MY_DEVICE = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
}

# conn = IOSXEDriver(**MY_DEVICE)
# conn.open()
# response = conn.send_command("show ip interface brief")
# print(response.result)
# conn.close()

with IOSXEDriver(**MY_DEVICE) as conn:
    response = conn.send_command("show ip interface brief")
print(response.result)
