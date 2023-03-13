from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")


def load_vars(task):
    group_data = task.run(
        task=load_yaml, file=f"./group_vars/{task.host['vendor']}.yaml"
    )
    task.host["vars"] = group_data.result
    host_data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["vars"].update(host_data.result)


def generate_config(task):
    snmp_template = task.run(
        task=template_file,
        template="snmp.j2",
        path=f"./templates/{task.host['vendor']}/",
    )
    snmp_result = snmp_template.result
    snmp_config = snmp_result.splitlines()
    task.run(task=netmiko_send_config, config_commands=snmp_config)


load_results = nr.run(task=load_vars)
config_results = nr.run(task=generate_config)
print_result(load_results)
print_result(config_results)
