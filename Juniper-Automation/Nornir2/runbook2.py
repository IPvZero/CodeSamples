from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def push_some_config(task):
    task.run(
        task=netmiko_send_config,
        config_commands=[f"set snmp community {task.host['snmp']}"],
    )


result = nr.run(task=push_some_config)
print_result(result)
