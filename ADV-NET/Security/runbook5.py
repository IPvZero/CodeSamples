from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def pull_show_run(task):
    task.run(task=send_command, command="show run")

results = nr.run(task=pull_show_run)
print_result(results)
