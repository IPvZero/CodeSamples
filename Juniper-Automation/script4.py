from scrapli import Scrapli

my_device = {
    "host": "192.168.4.101",
    "auth_username": "john",
    "auth_password": "Juniper1",
    "auth_strict_key": False,
    "platform": "juniper_junos",
}

conn = Scrapli(**my_device)
conn.open()
result = conn.send_configs_from_file(file="R1.cfg")
print(result.result)
conn.close()
