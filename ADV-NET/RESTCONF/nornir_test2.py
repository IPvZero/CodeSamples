import requests
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")
requests.packages.urllib3.disable_warnings()

headers = {"Accept": "application/yang-data+json"}


def restconf_test(task):
    url = f"https://{task.host.hostname}:443/restconf/data/openconfig-interfaces:interfaces"
    response = requests.get(
        url=url,
        headers=headers,
        auth=(f"{task.host.username}", f"{task.host.password}"),
        verify=False,
    )
    task.host["facts"] = response.json()
    asn = task.host["facts"]["Cisco-IOS-XE-bgp:neighbor"]["remote-as"]
    peer_id = task.host["facts"]["Cisco-IOS-XE-bgp:neighbor"]["id"]
    print(f"Neighbor {peer_id} is part of remote asn {asn}")
    return Result(host=task.host, result=response.text)


results = nr.run(task=restconf_test)
# print_result(results)
# import ipdb
# ipdb.set_trace()
