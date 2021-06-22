from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")


def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show ip interface")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    multicast_groups = task.host["facts"]["GigabitEthernet0/1"]["multicast_groups"]
    for multicast_ip in multicast_groups:
        if multicast_ip == "224.0.0.10":
            rprint(f"{task.host}'s int G0/1 has EIGRP enabled")


results = nr.run(task=pull_structured_data)
# print_result(results)
# ipdb.set_trace()
