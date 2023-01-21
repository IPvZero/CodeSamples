from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_pyez.plugins.tasks import pyez_facts

nr = InitNornir(config_file="config.yaml")


def test_stuff(task):
    response = task.run(task=pyez_facts)
    print(response.result["hostname"])


results = nr.run(task=test_stuff)
# print_result(results)
