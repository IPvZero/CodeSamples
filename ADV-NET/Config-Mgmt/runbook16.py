from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def ping_test(task):
    task.run(task=napalm_ping, dest="77.77.77.77")

results = nr.run(task=ping_test)
print_result(results)
