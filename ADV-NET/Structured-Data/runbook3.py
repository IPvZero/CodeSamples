from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")


def test_this(task):
    interfaces_result = task.run(task=send_command, command="show ip interface")
    task.host["facts"] = interfaces_result.scrapli_response.genie_parse_output()


results = nr.run(task=test_this)
print_result(results)
ipdb.set_trace()
