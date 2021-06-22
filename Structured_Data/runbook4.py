from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs

nr = InitNornir(config_file="config.yaml")


def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show cdp neighbor")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    cdp_index = task.host["facts"]["cdp"]["index"]
    for num in cdp_index:
        local_intf = cdp_index[num]["local_interface"]
        remote_port = cdp_index[num]["port_id"]
        remote_device = cdp_index[num]["device_id"]
        # rprint(f"{task.host} {local_intf} is connected to {remote_device} {remote_port}")
        config_commands = [
            f"interface {local_intf}",
            f"description Connected to {remote_device} via its {remote_port}",
        ]
        task.run(task=send_configs, configs=config_commands)


results = nr.run(task=pull_structured_data)
print_result(results)
