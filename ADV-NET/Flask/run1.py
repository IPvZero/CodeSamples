from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

results = nr.run(task=send_command, command="show version")
my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
for data in my_list:
    rprint(data["version"]["hostname"])

#my_list = []
#for v in results.values():
#    my_list.append(v.scrapli_response.result)
#print(my_list)
