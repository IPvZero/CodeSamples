"""Test OSPF Configurations on Juniper VMX"""

from collections import defaultdict
import ipaddress

from netmiko import ConnectHandler
from rich import print as rprint
import xmltodict

from inv import DEVICES


def gather_ospf(host, username, password):
    """Get OSPF"""

    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        ospf_xml = conn.send_command(
            command_string="show ospf interface detail | display xml"
        )
        return xmltodict.parse(ospf_xml)["rpc-reply"]["ospf-interface-information"][
            "ospf-interface"
        ]


def parse_ospf(config_dict, hostname, ospf_xml):
    """Parse OSPF"""

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

        config_dict[hostname][interface_name] = [
            area_id,
            str(ospf_network),
            mtu,
            hello_interval,
            dead_interval,
            stub_flag,
            ospf_auth,
        ]


def compare_ospf(
    config_dict, warning_list, local_hostname, local_intf, remote_hostname, remote_intf
):
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

    for local_var, remote_var, description in zip(
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
        if local_var != remote_var:
            warning_list.append(
                f"{local_intf} {local_hostname} {description} {local_var} != {remote_intf} {remote_hostname} {description} {remote_var}"
            )


def find_juniper_lldp(config_dict, warning_list, hostname, host, username, password):
    """Get LLDP Neighbor Info"""

    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        result = conn.send_command(command_string="show lldp neighbors | display xml")
        structured_interfaces = xmltodict.parse(result)
        for interface in structured_interfaces["rpc-reply"][
            "lldp-neighbors-information"
        ]["lldp-neighbor-information"]:
            remote_hostname = interface["lldp-remote-system-name"]
            local_intf = interface["lldp-local-port-id"]
            remote_intf = interface["lldp-remote-port-id"]

            compare_ospf(
                config_dict=config_dict,
                warning_list=warning_list,
                local_hostname=hostname,
                local_intf=local_intf,
                remote_hostname=remote_hostname,
                remote_intf=remote_intf,
            )


def get_rids(host, username, password, rid_list):
    """Get OSPF RIDs"""

    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        overview_xml = conn.send_command(
            command_string="show ospf overview | display xml"
        )
        overview_dict = xmltodict.parse(overview_xml)["rpc-reply"][
            "ospf-overview-information"
        ]["ospf-overview"]
        rid_list.append(overview_dict["ospf-router-id"])


def main():
    """Main Function"""

    config_dict = defaultdict(dict)
    warning_list = []
    rid_list = []
    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        username = device["username"]
        password = device["password"]
        ospf_xml = gather_ospf(host=host, username=username, password=password)
        parse_ospf(config_dict=config_dict, hostname=hostname, ospf_xml=ospf_xml)

    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        username = device["username"]
        password = device["password"]
        find_juniper_lldp(
            config_dict=config_dict,
            warning_list=warning_list,
            hostname=hostname,
            host=host,
            username=username,
            password=password,
        )
        get_rids(host=host, username=username, password=password, rid_list=rid_list)

    duplicates = set([rid for rid in rid_list if rid_list.count(rid) > 1])
    if duplicates:
        rprint(f"Warning: duplicate RIDs in the network: {duplicates}")

    if warning_list:
        for warning in warning_list:
            rprint(warning)

    elif not duplicates and not warning_list:
        rprint("[green]No problems detected[/green]")


if __name__ == "__main__":
    main()
