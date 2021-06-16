from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

command_list = ["show ip interface brief", "show version", "show run"]

def show_command_test(task):
    for cmd in command_list:
        task.run(task=send_command, command=cmd)

results = nr.run(task=
