from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=["get_facts"])
    task.host["facts"] = interfaces_result.result


results = nr.run(task=pull_interfaces_info)
print_result(results)
import ipdb

ipdb.set_trace()
