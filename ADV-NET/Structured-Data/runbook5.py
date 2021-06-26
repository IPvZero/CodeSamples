from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=["get_interfaces"])


results = nr.run(task=pull_interfaces_info)
print_result(results)
