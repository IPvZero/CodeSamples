import json
import logging
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")


def new_random_test(task):
    configuration = task.run(
        task=netmiko_send_command,
        severity_level=logging.DEBUG,
        command_string="show configuration interfaces | display json",
    )
    dict_configuration = json.loads(configuration.result)
    interface = dict_configuration["configuration"]["interfaces"]["interface"]
    result_list = []
    for intf in interface:
        target_interface = intf["name"]
        unit = intf["unit"]
        for element in unit:
            names = element["family"]["inet"]["address"]
            for name in names:
                ip = name["name"]
        result_list.append(f"{target_interface} has an IP address of {ip}")
    return Result(host=task.host, result=result_list)


result = nr.run(task=new_random_test)
print_result(result)
