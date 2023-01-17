from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def test_some_config(task):
    task.run(task=netmiko_send_command, command_string="show configuration")


not_central_devices = nr.filter(~F(longitude="central"))
results = not_central_devices.run(task=test_some_config)
print_result(results)
