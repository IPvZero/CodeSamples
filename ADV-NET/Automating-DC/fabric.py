import logging
import json
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file, send_command, send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def splatter(task):
    task.run(task=send_configs_from_file, file="basepusher.txt")
    load_vars(task)

def load_vars(task):
    loader = task.run(task=load_yaml, file=f"host_vars/{task.host}.yaml")
    task.host["facts"] = loader.result
    push_ospf(task)

def push_ospf(task):
    template = task.run(task=template_file, template="ospf.j2", path="templates")
    task.host["ospf_config"] = template.result
    rendered = task.host["ospf_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
    push_bgp(task)

def push_bgp(task):
    template = task.run(task=template_file, template="bgp.j2", path="templates")
    task.host["bgp_config"] = template.result
    rendered = task.host["bgp_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
    get_cdp(task)

def get_cdp(task):
    interfaces_list = []

    interfaces_result = task.run(
        task=send_command,
        command="show interface brief | json",
        severity_level=logging.DEBUG,
    )
    task.host["interfaces_facts"] = json.loads(interfaces_result.result)
    interfaces = task.host["interfaces_facts"]["TABLE_interface"]["ROW_interface"]
    for interface in interfaces:
        intf = interface["interface"]
        if intf not in ("mgmt0", "loopback0"):
            interfaces_list.append(intf)

    cdp_result = task.run(
        task=send_command,
        command="show cdp neighbor | json",
        severity_level=logging.DEBUG,
    )
    task.host["cdp_facts"] = json.loads(cdp_result.result)
    connections = task.host["cdp_facts"]["TABLE_cdp_neighbor_brief_info"][
        "ROW_cdp_neighbor_brief_info"
    ]
    for device in connections:
        platform = device["platform_id"]
        if platform == "N9K-9000v":
            local_intf = device["intf_id"]
            interfaces_list.remove(local_intf)
    clean_up(task, interfaces_list)


def clean_up(task, interfaces_list):
    for interface in interfaces_list:
        task.run(
            task=send_configs,
            configs=[
                f"interface {interface}",
                "switchport",
                "shutdown",
                "description SHUTDOWN",
            ],
        )


results = nr.run(task=splatter)
print_result(results)
