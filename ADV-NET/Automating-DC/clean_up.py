import json
from rich import print as rprint
from nornir import InitNornir
from nornir_scrapli.tasks import send_command, send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def get_cdp(task):
    interfaces_list = []
    interfaces_result = task.run(task=send_command, command="show interface brief | json")
    task.host["interfaces_facts"] = json.loads(interfaces_result.result)
    interfaces = task.host["interfaces_facts"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        intf = interface["interface"]
        if intf not in ("mgmt0", "loopback0"):
            interfaces_list.append(intf)
    
    cdp_result = task.run(task=send_command, command="show cdp neighbor | json")
    task.host["cdp_facts"] = json.loads(cdp_result.result)
    connections = task.host["cdp_facts"]["TABLE_cdp_neighbor_brief_info"]["ROW_cdp_neighbor_brief_info"]
    for device in connections:
        platform = device["platform_id"]
        if platform == "N9K-9000v":
            local_intf = device["intf_id"]
            interfaces_list.remove(local_intf)
    clean_interfaces(task, interfaces_list)

def clean_interfaces(task, interfaces_list):
    for interface in interfaces_list:
        task.run(task=send_configs, configs=[f"interface {interface}", "switchport", "shutdown", "description SHUTDOWN"])



results = nr.run(task=get_cdp)
print_result(results)
#import ipdb
#ipdb.set_trace()
