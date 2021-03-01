from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def replace_stuff(task):
    task.run(task=napalm_configure, filename=f"backup-directory/{task.host}.txt", replace=True)

results = nr.run(task=replace_stuff)
print_result(results)
