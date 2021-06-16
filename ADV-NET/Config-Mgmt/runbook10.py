from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def another_config_test(task):
    task.run(task=netmiko_send_config, config_commands=["ntp server 11.22.11.22"])


results = nr.run(task=another_config_test)
print_result(results)
