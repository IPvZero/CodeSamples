from collections import defaultdict
import ipaddress

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as rprint
import xmltodict

nr = InitNornir(config_file="config.yaml")
my_list = []


def connect_junos(task):
    junos_results = task.run(
        task=netmiko_send_command,
        command_string="show configuration interfaces | display xml",
    ).result
    parse_junos(task, junos_results)


def connect_cisco(task):
    dict_interfaces = task.run(
        task=netmiko_send_command,
        command_string="show ip interface brief",
        use_genie=True,
    ).result["interface"]
    parse_cisco(task, dict_interfaces)


def parse_junos(task, junos_results):
    result_dict = xmltodict.parse(junos_results)
    interfaces = result_dict["rpc-reply"]["configuration"]["interfaces"]["interface"]
    for intf in interfaces:
        try:
            addresses = intf["unit"]["family"]["inet"]["address"]
            if isinstance(addresses, list):
                for address in addresses:
                    ip_addy = address["name"]
                    ip = ipaddress.IPv4Address(ip_addy.split("/")[0])
                    my_list.append({task.host["device_name"]: str(ip)})
            else:
                ip_addy = addresses["name"]
                ip = ipaddress.IPv4Address(ip_addy.split("/")[0])
                my_list.append({task.host["device_name"]: str(ip)})
        except (KeyError, TypeError):
            pass


def parse_cisco(task, dict_interfaces):
    for interface in dict_interfaces:
        ip_addy = dict_interfaces[interface]["ip_address"]
        try:
            ipaddress.IPv4Address(ip_addy)
            my_list.append({task.host["device_name"]: str(ip_addy)})
        except ipaddress.AddressValueError:
            pass


junos_nr = nr.filter(platform="juniper_junos")
cisco_nr = nr.filter(platform="cisco_ios")
juniper_results = junos_nr.run(task=connect_junos)
cisco_results = cisco_nr.run(task=connect_cisco)

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
