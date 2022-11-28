from netmiko import ConnectHandler
from rich import print as rprint
from inventory import DEVICES

def configure_device(hostname):
    my_list_configs = ["set snmp community BLAHBLAHBLAH", "set snmp community BLAH2"]
    with ConnectHandler(device_type="juniper", host=hostname, username="john", password="Juniper1", port=22) as conn:
        conn.send_config_set(config_commands=my_list_configs)
        compare_result = conn.send_config_set(config_commands=["show | compare"])
        rprint(compare_result)

def rollback_device(hostname):
    with ConnectHandler(device_type="juniper", host=hostname, username="john", password="Juniper1", port=22) as conn:
        rollback_result = conn.send_config_set(config_commands=["rollback 0", "commit confirmed 1", "commit"])
        rprint(rollback_result)

def commit_device(hostname):
    with ConnectHandler(device_type="juniper", host=hostname, username="john", password="Juniper1", port=22) as conn:
        commit_result = conn.send_config_set(config_commands=["commit confirmed 1", "commit"])
        rprint(commit_result)

def main():
    for device in DEVICES:
        hostname = device["hostname"]
        configure_device(hostname)

    answer = input("Do you want to commit these changes to all devices? <y/n> ")
    if answer == "y":
        for device in DEVICES:
            hostname = device["hostname"]
            commit_device(hostname)
    else:
        for device in DEVICES:
            hostname = device["hostname"]
            rollback_device(hostname)

main()


