"""
Author: IPvZero
"""


import logging
import os
import threading
from collections import Counter
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

LOCK = threading.Lock()

CLEAR = "clear"
os.system(CLEAR)
ip_list = []
filtered = False

os.system(CLEAR)
answer = input("Would you like to apply a location filter to this script? <y/n> ")
if answer == "y":
    location = input("Select a location to target: ")
    filtered = True
    filter_type = input(
        "Do you want to include or exclude this location?: <include/exclude> "
    )
    if filter_type == "exclude":
        filtered_hosts = nr.filter(~F(location=location))
    else:
        filtered_hosts = nr.filter(F(location=location))


def get_ip(task):
    """
    Parse IP addresses from all interfaces and append to ip_list
    """
    response = task.run(
        task=send_command, command="show interfaces", severity_level=logging.DEBUG
    )
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                ip_list.append(ip_addr)
        except KeyError:
            pass


def locate_ip(task):
    """
    Pull all interfaces information
    Identify the interface and Device configured with duplicate address
    """
    response = task.run(
        task=send_command, command="show interfaces", severity_level=logging.DEBUG
    )
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for intf in interfaces:
        try:
            ip_key = interfaces[intf]["ipv4"]
            for ip in ip_key:
                ip_addr = ip_key[ip]["ip"]
                if ip_addr in targets:
                    version_result = task.run(
                        task=send_command,
                        command="show version",
                        severity_level=logging.DEBUG,
                    )
                    task.host[
                        "verfacts"
                    ] = version_result.scrapli_response.textfsm_parse_output()
                    serial = task.host["verfacts"][0]["serial"][0]
                    data = task.host.data
                    LOCK.acquire()
                    rprint(f"[yellow]{task.host} {intf} - {ip_addr}[/yellow]")
                    rprint("[cyan]RETRIEVING DEVICE DATA...[/cyan]")
                    print(f"SERIAL NUMBER: {serial}")
                    print(f"MGMT IP: {task.host.hostname}")
                    for k, v in data.items():
                        if "facts" not in k:
                            print(f"{k} = {v}")
                    print("\n")
                    LOCK.release()

        except KeyError:
            pass


if filtered:
    filtered_hosts.run(task=get_ip)
    targets = [k for k, v in Counter(ip_list).items() if v > 1]
    if targets:
        rprint("[red]ALERT: DUPLICATES DETECTED![/red]")
        rprint(targets)
        rprint("\n[cyan]Locating addresses in topology...[/cyan]\n")
        filtered_hosts.run(task=locate_ip)
    else:
        rprint("[green]SCAN COMPLETED - NO DUPLICATES DETECTED[/green]")
else:
    nr.run(task=get_ip)
    targets = [k for k, v in Counter(ip_list).items() if v > 1]
    if targets:
        rprint("[red]ALERT: DUPLICATES DETECTED![/red]")
        rprint(targets)
        rprint("\n[cyan]Locating addresses in topology...[/cyan]\n")
        nr.run(task=locate_ip)
    else:
        rprint("[green]SCAN COMPLETED - NO DUPLICATES DETECTED[/green]")
