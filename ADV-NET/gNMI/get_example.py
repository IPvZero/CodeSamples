from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from pygnmi.client import gNMIclient

nr = InitNornir(config_file="config.yaml")

yang_path = ["openconfig-interfaces:interfaces"]

def test(task, path):
    with gNMIclient(
        target=(task.host.hostname, task.host.port),
        username=task.host.username,
        password=task.host.password,
        insecure=True,
    ) as client:
        response = client.get(path=path)
    return Result(host=task.host, result=response)


results = nr.run(task=test, path=yang_path)
print_result(results)
