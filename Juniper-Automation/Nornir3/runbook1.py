from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
import ipdb

nr = InitNornir(config_file="config.yaml")


def load_my_vars(task):
    host_data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["host_vars"] = host_data.result
    group_data = task.run(
        task=load_yaml, file=f"./group_vars/{task.host['vendor']}.yaml"
    )
    task.host["group_vars"] = group_data.result


nr.run(task=load_my_vars)
ipdb.set_trace()
