from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def test_this(task):
    clock_results = task.run(task=send_command, command="show version")
    structured_output = clock_results.scrapli_response.textfsm_parse_output()
    # print(structured_output)


results = nr.run(task=test_this)
print_result(results)
