from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

commands = input("\nEnter Commands You Wish To Send: ")
cmds = commands.split(",")

def push_show_commands(task):
    for cmd in cmds:
        task.run(task=send_command, command=cmd)

results = nr.run(task=push_show_commands)
