"""
Script to retrieve MAC address from network
"""

import sys

from netaddr import EUI
from netaddr.core import AddrFormatError
from netmiko import ConnectHandler
from rich import print as rprint
import xmltodict

from inv import DEVICES


def validate_mac_address(target_mac):
    """Validate MAC Address entered is valid"""

    try:
        target_mac = EUI(target_mac)
        return target_mac
    except (ValueError, TypeError, AddrFormatError):
        print("Invalid Mac Address Entered!")
        sys.exit(1)


def connect_junos_device(host, username, password):
    """Get interface info from Juniper devices"""

    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        results = conn.send_command(command_string="show interfaces | display xml")
        structured_interfaces = xmltodict.parse(results)["rpc-reply"][
            "interface-information"
        ]["physical-interface"]
        return structured_interfaces


def connect_cisco_device(host, username, password):
    """Get interface info from Cisco devices"""

    with ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        structured_interfaces = conn.send_command(
            command_string="show interfaces", use_genie=True
        )
        return structured_interfaces


def find_junos_mac(
    structured_interfaces,
    hostname,
    host,
    username,
    password,
    device_type,
    target_mac,
):
    """Attempt to locate MAC address on Juniper device"""

    dict_result = {}
    for interface in structured_interfaces:
        try:
            mac_address = interface["current-physical-address"]
            name = interface["name"]
            if target_mac == mac_address:
                dict_result["local_interface"] = name
                dict_result["hostname"] = hostname
                dict_result["host"] = host
                dict_result["username"] = username
                dict_result["password"] = password
                dict_result["device_type"] = device_type

        except KeyError:
            pass
    return dict_result


def find_cisco_mac(
    structured_interfaces,
    hostname,
    host,
    username,
    password,
    device_type,
    target_mac,
):
    """Attempt to locate MAC address on Juniper device"""

    dict_result = {}
    for interface in structured_interfaces:
        try:
            mac_address = structured_interfaces[interface]["mac_address"]
            if target_mac == mac_address:
                dict_result["local_interface"] = interface
                dict_result["hostname"] = hostname
                dict_result["host"] = host
                dict_result["username"] = username
                dict_result["password"] = password
                dict_result["device_type"] = device_type
        except KeyError:
            pass
    return dict_result


def determine_device_type(dict_result, target_mac):
    """Once MAC has been located, determine device type"""

    if dict_result["device_type"] == "juniper_junos":
        find_juniper_lldp(dict_result, target_mac)
    elif dict_result["device_type"] == "cisco_ios":
        find_cisco_lldp(dict_result, target_mac)


def find_juniper_lldp(dict_result, target_mac):
    """If MAC found on Juniper device,
    attempt to find its remote connection via LLDP"""

    hostname = dict_result["hostname"]
    local_interface = dict_result["local_interface"]
    host = dict_result["host"]
    username = dict_result["username"]
    password = dict_result["password"]

    rprint(f"[green]{target_mac} found on {hostname}'s {local_interface}[/green]")
    rprint("[yellow]Determining any potential connections...[/yellow]")
    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        result = conn.send_command(command_string="show lldp neighbors | display xml")
        structured_interfaces = xmltodict.parse(result)
        has_remote_connections = False
        for interface in structured_interfaces["rpc-reply"][
            "lldp-neighbors-information"
        ]["lldp-neighbor-information"]:
            local_intf = interface["lldp-local-port-id"]
            if local_intf == local_interface:
                remote_intf = interface["lldp-remote-port-id"]
                remote_hostname = (
                    interface["lldp-remote-system-name"].split(".")[0].strip()
                )
                print(
                    f"{local_interface} is connected to {remote_hostname}'s {remote_intf}"
                )
                has_remote_connections = True
        if not has_remote_connections:
            print("No remote connections detected")


def find_cisco_lldp(dict_result, target_mac):
    """If MAC found on Cisco device,
    attempt to find its remote connection via LLDP"""

    hostname = dict_result["hostname"]
    local_interface = dict_result["local_interface"]
    host = dict_result["host"]
    username = dict_result["username"]
    password = dict_result["password"]

    rprint(f"[green]{target_mac} found on {hostname}'s {local_interface}[/green]")
    rprint("[yellow]Determining any potential connections...[/yellow]")
    with ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        structured_interfaces = conn.send_command(
            command_string="show lldp neighbors", use_genie=True
        )["interfaces"]

        try:
            remote_keys = structured_interfaces[local_interface]["port_id"].keys()
            for remote_intf in remote_keys:
                neighbors = structured_interfaces[local_interface]["port_id"][
                    remote_intf
                ]["neighbors"].keys()
            for neighbor in neighbors:
                remote_hostname = neighbor.split(".")[0].strip()
                print(
                    f"{local_interface} is connected to {remote_hostname}'s {remote_intf}"
                )

        except KeyError:
            print("No remote connections detected")


def main():
    """Main execution point"""

    target_mac = input("Enter the MAC address you wish to target: ")
    target_mac = validate_mac_address(target_mac)
    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        username = device["username"]
        password = device["password"]
        device_type = device["device_type"]
        if device_type == "juniper_junos":
            structured_interfaces = connect_junos_device(
                host=host, username=username, password=password
            )
            dict_result = find_junos_mac(
                structured_interfaces=structured_interfaces,
                hostname=hostname,
                host=host,
                username=username,
                password=password,
                device_type=device_type,
                target_mac=target_mac,
            )

        elif device_type == "cisco_ios":
            structured_interfaces = connect_cisco_device(
                host=host, username=username, password=password
            )
            dict_result = find_cisco_mac(
                structured_interfaces=structured_interfaces,
                hostname=hostname,
                host=host,
                username=username,
                password=password,
                device_type=device_type,
                target_mac=target_mac,
            )

        if dict_result:
            determine_device_type(dict_result, target_mac)
            return
    print(f"No device found with MAC Address {target_mac}")


if __name__ == "__main__":
    main()
