"""
Author: IPvZero
"""

import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import json
from nornir.core.filter import F
from ipaddress import ip_network, ip_address
from rich import print as rprint

CLEAR = "clear"
os.system(CLEAR)
nr = InitNornir(config_file="config.yaml")

target = input("Enter the target IP: ")
ipaddr = ip_address(target)
my_list = []

def get_cisco(task):
    """
    Parse routing table and determine if target IP finds a match
    """
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        my_list.append(
                            f"{task.host} is connected to {target} via interface {exit_intf}"
                        )
                except KeyError:
                    pass
            else:
                try:
                    next_hop_list = prefixes[prefix]["next_hop"]["next_hop_list"]
                    route_preference = prefixes[prefix]["route_preference"]
                    for key in next_hop_list:
                        next_hop = next_hop_list[key]["next_hop"]
                        if route_preference == 20:
                            source_proto = "eBGP"
                        elif route_preference == 200:
                            source_proto = "iBGP"
                        my_list.append(
                            (
                                f"{task.host} can reach {target} via "
                                f"next hop: {next_hop} ({source_proto})"
                            )
                        )
                except KeyError:
                    pass


def get_arista(task):
    result = task.run(task=send_command, command="show ip route | json")
    task.host["facts"] = json.loads(result.result)
    prefixes = task.host["facts"]["vrfs"]["default"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            route_type = prefixes[prefix]["routeType"]
            vias = prefixes[prefix]["vias"]
            for via in vias:
                exit_intf = via["interface"]
                if route_type == "connected":
                    my_list.append(
                            f"{task.host} is connected to {target} via interface {exit_intf}"
                    )
                else:
                    next_hop = via["nexthopAddr"]
                    my_list.append(
                        (
                            f"{task.host} can reach {target} via "
                            f"next hop: {next_hop} ({route_type})"
                        )
                    )


cisco = nr.filter(F(platform="ios"))
cisco.run(task=get_cisco)
arista = nr.filter(F(platform="eos"))
arista.run(task=get_arista)
if my_list:
    sorted_list = sorted(my_list)
    rprint(sorted_list)
else:
    rprint(f"{target} is not reachable")
