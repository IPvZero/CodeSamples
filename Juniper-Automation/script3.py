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
mycommands = ["show configuration system", "show interfaces terse"]
result = conn.send_commands(commands=mycommands)
print(result.result)
conn.close()
