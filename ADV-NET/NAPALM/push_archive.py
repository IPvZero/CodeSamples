from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

def test(task):
    task.run(task=send_configs_from_file, file="napalm-startup.txt")


results = nr.run(task=test)
print_result(results)
