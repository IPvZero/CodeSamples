from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")


def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show version")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    version_number = task.host["facts"]["version"]["version_short"]
    if version_number == "15.8":
        rprint(f"{task.host}: [green]VERSION CHECK PASSED[/green]")
    else:
        rprint(f"{task.host}: [red]VERSION CHECK FAILED[/red]")


results = nr.run(task=pull_structured_data)
# print_result(results)
# ipdb.set_trace()
