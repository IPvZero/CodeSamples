"""
python3 -m pip install nornir-scrapli
python3 -m pip install rich
"""


import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
target_list = []

CLEAR = "clear"
os.system(CLEAR)

target = input("Enter the mac address that you wish to find: ")


def pull_info(task):
    """
    Pull show interfaces
    Parse data & test for target match
    """

    interface_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = interface_result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for interface in interfaces:
        try:
            mac_addr = interfaces[interface]["mac_address"]
            if target == mac_addr:
                target_list.append(mac_addr)
                intf = interface
                print_info(task, intf)
        except KeyError:
            pass


def print_info(task, intf):
    """
    Pull show cdp neighbor and show version
    Parse data & test for remote connection
    """

    rprint("\n[green]*** TARGET IDENTIFIED ***[/green]")
    print(f"MAC ADDRESS: {target} is present on {task.host}'s {intf}")
    rprint("\n[cyan]GENERATING DETAILS...[/cyan]")
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
    dev_id = ""
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]

    ver_result = task.run(task=send_command, command="show version")
    task.host["verinfo"] = ver_result.scrapli_response.genie_parse_output()
    version = task.host["verinfo"]["version"]
    serial_num = version["chassis_sn"]
    oper_sys = version["os"]
    uptime = version["uptime"]
    version_short = version["version_short"]
    print(f"DEVICE MGMT IP: {task.host.hostname}")
    print(f"DEVICE SERIAL NUMBER: {serial_num}")
    print(f"DEVICE OPERATION SYSTEM: {oper_sys}")
    print(f"DEVICE UPTIME: {uptime}")
    print(f"DEVICE VERSION: {version_short}")
    if dev_id:
        rprint("[cyan]REMOTE CONNECTION DETAILS...[/cyan]")
        print(f"Connected to {port_id} on {dev_id}")


nr.run(task=pull_info)
if target not in target_list:
    rprint("[red]TARGET NOT FOUND[/red]")
