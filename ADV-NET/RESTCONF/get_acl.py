import requests
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")
requests.packages.urllib3.disable_warnings()

headers = {"Accept": "application/yang-data+json"}


def restconf_test(task):
    url = f"https://{task.host.hostname}:443/restconf/data/openconfig-acl:acl?content=config"
    response = requests.get(
        url=url,
        headers=headers,
        auth=(f"{task.host.username}", f"{task.host.password}"),
        verify=False,
    )
    return Result(host=task.host, result=response.text)


results = nr.run(task=restconf_test)
print_result(results)
