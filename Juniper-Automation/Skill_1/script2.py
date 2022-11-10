from netmiko import ConnectHandler

my_device = {
    "device_type": "juniper",
    "host": "192.168.4.102",
    "username": "john",
    "password": "Juniper1",
    "port": 22,
}

conn = ConnectHandler(**my_device)
result = conn.send_config_from_file(config_file="R2.cfg")
print(result)
