from scrapli import Scrapli

def connect_junos(device_ip):
    device = {
        "host": device_ip,
        "auth_username": "john",
        "auth_password": "Juniper1",
        "auth_strict_key": False,
        "platform": "juniper_junos"
    }
    conn = Scrapli(**device)
    conn.open()
    result = conn.send_command("show configuration")
    return result.result

result = connect_junos("192.168.4.101")
print(result)