from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")


def test_this(task):
    interfaces_result = task.run(
        task=netmiko_send_command, command_string="show ip interface", use_genie=True
    )
    task.host["facts"] = interfaces_result.result


results = nr.run(task=test_this)
print_result(results)
ipdb.set_trace()
