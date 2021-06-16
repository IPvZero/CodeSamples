from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
command_list = ["show version", "show ntp config", "show ip int brief"]

def another_show_command_test(task):
    for cmd in command_list:
        task.run(task=netmiko_send_command, command_string=cmd)

results = nr.run(task=another_show_command_test)
print_result(results)
