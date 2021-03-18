from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def push_baseconfig(task):
    task.run(task=send_configs_from_file, file="basepusher.txt")

results = nr.run(task=push_baseconfig)
print_result(results)
