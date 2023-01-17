from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def test_some_config(task):
    task.run(task=netmiko_send_command, command_string="show configuration")


north_devices = nr.filter(F(latitude="north") | F(platform="juniper_junos"))
results = north_devices.run(task=test_some_config)
print_result(results)
