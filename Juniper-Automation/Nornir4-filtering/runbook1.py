from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")


def print_stuff(task):
    if task.host["latitude"] != "south":
        return
    else:
        return Result(host=task.host, result="This device is in the South of the USA")


results = nr.run(task=print_stuff)
print_result(results)
