from collections import defaultdict
from email.policy import default
import ipaddress
from netmiko import ConnectHandler
import xmltodict
from rich import print as rprint
from pprint import pprint
from inv import DEVICES


my_list = []


def connect_junos_device(host: str, username: str, password: str) -> str:
    with ConnectHandler(
        device_type="juniper_junos",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        interfaces_xml = conn.send_command(
            command_string="show configuration interfaces | display xml"
        )
        return interfaces_xml


def connect_cisco_device(host: str, username: str, password: str) -> dict:
    with ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=username,
        password=password,
        port=22,
    ) as conn:
        cisco_interfaces = conn.send_command(
            command_string="show ip interface brief", use_genie=True
        )
        return cisco_interfaces["interface"]


def parse_junos(hostname: str, interfaces_xml: str) -> None:
    result_dict = xmltodict.parse(interfaces_xml)
    interfaces = result_dict["rpc-reply"]["configuration"]["interfaces"]["interface"]
    for intf in interfaces:
        try:
            addresses = intf["unit"]["family"]["inet"]["address"]
            if isinstance(addresses, list):
                for address in addresses:
                    ip_addy = address["name"]
                    ip = ipaddress.IPv4Address(ip_addy.split("/")[0])
                    my_list.append({hostname: str(ip)})
            else:
                ip_addy = addresses["name"]
                ip = ipaddress.IPv4Address(ip_addy.split("/")[0])
                my_list.append({hostname: str(ip)})
        except (KeyError, TypeError):
            pass

        except KeyError:
            pass


def parse_cisco(hostname: str, cisco_interfaces: dict) -> None:
    for interface in cisco_interfaces:
        ip_addy = cisco_interfaces[interface]["ip_address"]
        try:
            ip = ipaddress.IPv4Address(ip_addy)
            my_list.append({hostname: str(ip)})
        except ipaddress.AddressValueError:
            pass


def main() -> None:
    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        username = device["username"]
        password = device["password"]
        device_type = device["device_type"]
        if device_type == "juniper_junos":
            interfaces_xml = connect_junos_device(
                host=host, username=username, password=password
            )
            parse_junos(hostname, interfaces_xml)

        elif device_type == "cisco_ios":
            cisco_interfaces = connect_cisco_device(
                host=host, username=username, password=password
            )
            parse_cisco(hostname, cisco_interfaces)

    ip_dictionary = defaultdict(list)
    for dictionary in my_list:
        for k, v in dictionary.items():
            ip_dictionary[v].append(k)

    duplicate_dict = {}
    for k, v in ip_dictionary.items():
        if len(v) > 1:
            duplicate_dict[k] = v

    if duplicate_dict:
        rprint(duplicate_dict)
    else:
        rprint("[green]No duplicate IP addresses found [/green]")


if __name__ == "__main__":
    main()
