import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
north_password = getpass.getpass(prompt="Enter the North Group password: ")
south_password = getpass.getpass(prompt="Enter the South Group password: ")
r7_password = getpass.getpass(prompt="Enter R7's password: ")

nr.inventory.groups["north"].password = north_password
nr.inventory.groups["south"].password = south_password
nr.inventory.hosts["R7"].password = r7_password


def credential_test(task):
    task.run(task=send_command, command="show ip interface brief")

results = nr.run(task=credential_test)
print_result(results)
