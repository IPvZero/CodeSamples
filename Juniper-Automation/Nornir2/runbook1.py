from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def get_some_stuff(task):
    task.run(task=netmiko_send_command, command_string="show configuration")


result = nr.run(task=get_some_stuff)
print_result(result)
