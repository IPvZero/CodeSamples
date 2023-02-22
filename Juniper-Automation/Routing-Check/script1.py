from ipaddress import ip_network, ip_address
from netmiko import ConnectHandler
import xmltodict
from pprint import pprint
from rich import print as rprint

from inv import DEVICES


target_ip = input("Enter the IP address you wish to locate: ")
ipaddr = ip_address(target_ip)


def gather_juniper_routing(host, username, password):
    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        routes_xml = conn.send_command(command_string="show route terse | display xml")
        return xmltodict.parse(routes_xml)["rpc-reply"]["route-information"][
            "route-table"
        ][0]["rt"]


def gather_cisco_routing(host, username, password):
    with ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        routes_dict = conn.send_command(command_string="show ip route", use_genie=True)
        return routes_dict["vrf"]["default"]["address_family"]["ipv4"]["routes"]


def parse_junos(hostname, routes_xml):
    unreachable = True
    for x in routes_xml:
        route = x["rt-destination"]
        if ipaddr in ip_network(route):
            unreachable = False
            if x["rt-entry"]["protocol-name"] == "Direct":
                next_hop = x["rt-entry"]["nh"]["via"]
                rprint(
                    f"{hostname} is directly connected to {target_ip} via {next_hop}"
                )

            elif x["rt-entry"]["protocol-name"] == "Local":
                rprint(f"{target_ip} is configured on {hostname}")

            elif x["rt-entry"]["protocol-name"] in ("BGP", "OSPF"):
                source_proto = x["rt-entry"]["protocol-name"]
                if "nh" in x["rt-entry"]:
                    next_hop = x["rt-entry"]["nh"]
                    if isinstance(next_hop, list):
                        for hop in next_hop:
                            rprint(
                                f"{hostname} can reach {route} via {hop['to']} ({source_proto})"
                            )
                    elif isinstance(next_hop, dict):
                        rprint(
                            f"{hostname} can reach {route} via {next_hop['to']} ({source_proto})"
                        )

    if unreachable:
        rprint(f"{hostname} cannot reach {target_ip}")


def parse_cisco(hostname, routes_dict):
    unreachable = True
    for prefix, route in routes_dict.items():
        network = ip_network(prefix)
        if ipaddr in network:
            unreachable = False
            source_proto = route["source_protocol"]
            if source_proto == "connected":
                outgoing_intf = route["next_hop"]["outgoing_interface"]
                for intf in outgoing_intf:
                    rprint(f"{hostname} is connected to {target_ip} via {intf}")

            elif source_proto == "local":
                rprint(f"{target_ip} is configured on {hostname}")

            else:
                next_hop_list = route["next_hop"]["next_hop_list"]
                for next_hop in next_hop_list.values():
                    hop = next_hop["next_hop"]
                    rprint(
                        f"{hostname} can reach {target_ip} via {hop} ({source_proto.upper()})"
                    )
    if unreachable:
        rprint(f"{hostname} cannot reach reach {target_ip}")


def main():
    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        username = device["username"]
        password = device["password"]
        device_type = device["device_type"]
        if device_type == "juniper_junos":
            routes_xml = gather_juniper_routing(
                host=host, username=username, password=password
            )
            parse_junos(hostname, routes_xml)

        elif device_type == "cisco_ios":
            routes_dict = gather_cisco_routing(
                host=host, username=username, password=password
            )
            parse_cisco(hostname, routes_dict)


if __name__ == "__main__":
    main()
