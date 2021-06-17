from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def rollin_rollin_rollin(task):
    task.run(task=send_command, command="configure replace flash:ipvzero force")

results = nr.run(task=rollin_rollin_rollin)
print_result(results)
