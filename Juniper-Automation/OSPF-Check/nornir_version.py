"""Test OSPF Configurations on Juniper VMX"""

from collections import defaultdict
import ipaddress

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as rprint
import xmltodict


nr = InitNornir(config_file="config.yaml")
config_dict = defaultdict(dict)
warning_list = []
rid_list = []


def gather_ospf(task):
    """GET OSPF"""
    response = task.run(
        task=netmiko_send_command,
        command_string="show ospf interface detail | display xml",
    ).result
    ospf_xml = xmltodict.parse(response)["rpc-reply"]["ospf-interface-information"][
        "ospf-interface"
    ]
    parse_ospf(task, ospf_xml)


def parse_ospf(task, ospf_xml):
    """PARSE OSPF"""
    for interface in ospf_xml:
        interface_name = interface["interface-name"][:-2]
        area_id = interface["ospf-area"]

        ip_addy = interface["interface-address"]
        mask = interface["address-mask"]
        ospf_network = ipaddress.IPv4Network(f"{ip_addy}/{mask}", strict=False)

        mtu = interface["mtu"]
        hello_interval = interface["hello-interval"]
        dead_interval = interface["dead-interval"]
        stub_flag = interface["ospf-stub-type"]
        ospf_auth = interface["authentication-type"]
        config_dict[task.host["device_name"]][interface_name] = [
            area_id,
            str(ospf_network),
            mtu,
            hello_interval,
            dead_interval,
            stub_flag,
            ospf_auth,
        ]


def compare_ospf(local_hostname, local_intf, remote_hostname, remote_intf):
    """Lookup Config Dict and Compare Links"""
    (
        local_area_id,
        local_ospf_net,
        local_mtu,
        local_hello,
        local_dead,
        local_stub,
        local_auth,
    ) = config_dict[local_hostname][local_intf]
    (
        remote_area_id,
        remote_ospf_net,
        remote_mtu,
        remote_hello,
        remote_dead,
        remote_stub,
        remote_auth,
    ) = config_dict[remote_hostname][remote_intf]

    for local_val, remote_val, label in zip(
        [
            local_area_id,
            local_ospf_net,
            local_mtu,
            local_hello,
            local_dead,
            local_stub,
            local_auth,
        ],
        [
            remote_area_id,
            remote_ospf_net,
            remote_mtu,
            remote_hello,
            remote_dead,
            remote_stub,
            remote_auth,
        ],
        ["Area", "Network", "MTU", "Hello", "Dead", "Stub", "Auth"],
    ):
        if local_val != remote_val:
            warning_list.append(
                f"{local_intf} {local_hostname} {label} {local_val} != {remote_intf} {remote_hostname} {label} {remote_val}"
            )


def find_juniper_lldp(task):
    """Get LLDP Neighbor Info"""

    response = task.run(
        task=netmiko_send_command, command_string="show lldp neighbors | display xml"
    ).result

    structured_interfaces = xmltodict.parse(response)

    for interface in structured_interfaces["rpc-reply"]["lldp-neighbors-information"][
        "lldp-neighbor-information"
    ]:
        remote_hostname = interface["lldp-remote-system-name"]
        local_intf = interface["lldp-local-port-id"]
        remote_intf = interface["lldp-remote-port-id"]

        compare_ospf(
            local_hostname=task.host["device_name"],
            local_intf=local_intf,
            remote_hostname=remote_hostname,
            remote_intf=remote_intf,
        )


def get_rids(task):
    """Get OSPF RIDs"""

    response = task.run(
        netmiko_send_command, command_string="show ospf overview | display xml"
    ).result

    overview_dict = xmltodict.parse(response)["rpc-reply"]["ospf-overview-information"][
        "ospf-overview"
    ]

    rid_list.append(overview_dict["ospf-router-id"])


gather_ospf = nr.run(task=gather_ospf)
find_juniper_lldp = nr.run(task=find_juniper_lldp)
get_rids = nr.run(task=get_rids)


duplicates = set([num for num in rid_list if rid_list.count(num) > 1])
if duplicates:
    rprint(f"Warning: duplicate RIDs in the network: {duplicates}")

if warning_list:
    for warning in warning_list:
        rprint(warning)
elif not duplicates and not warning_list:
    rprint("[green]No problems detected[/green]")
