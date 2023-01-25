import json
import logging
from nornir import InitNornir
from nornir_http.tasks import http_method
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def get_arp_info(task):
    endpoint = "/get-arp-table-information"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = task.run(
        task=http_method,
        method="post",
        url=f"http://{task.host.hostname}:8080/rpc{endpoint}",
        auth=("john", "Juniper1"),
        headers=headers,
        raise_for_status=True,
        severity_level=logging.DEBUG,
    )

    dict_response = json.loads(response.result)
    mac_addy = dict_response["arp-table-information"]["arp-table-entry"]["mac-address"]
    return Result(host=task.host, result=f"Connected to Device with MAC {mac_addy}")


results = nr.run(task=get_arp_info)
print_result(results)
