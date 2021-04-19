import requests
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")
requests.packages.urllib3.disable_warnings()
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
chained_url = "data/openconfig-acl:acl"


def load_data(task):
    data = task.run(task=load_yaml, file=f"host_vars/{task.host}.yaml")
    task.host["facts"] = data.result


def configure_stuff(task, chained_url, headers):
    restconf_url = f"https://{task.host.hostname}:443/restconf/"

    response = requests.put(
        url=restconf_url + chained_url,
        headers=headers,
        auth=(f"{task.host.username}", f"{task.host.password}"),
        verify=False,
        json=task.host["facts"]["configure_acl"],
    )
    return Result(host=task.host, result=response)


load_results = nr.run(task=load_data)
print_result(load_results)
configure_results = nr.run(
    task=configure_stuff, chained_url=chained_url, headers=headers
)
print_result(configure_results)
