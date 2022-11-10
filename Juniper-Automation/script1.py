from netmiko import ConnectHandler

my_device = {
    "device_type": "juniper",
    "host": "192.168.4.102",
    "username": "john",
    "password": "Juniper1",
    "port": 22,
}

conn = ConnectHandler(**my_device)
my_list_of_configs = [
    "set system host-name R2-UPDATED",
    "set snmp community IPvZero",
    "commit",
]
result = conn.send_config_set(config_commands=my_list_of_configs)
print(result)
