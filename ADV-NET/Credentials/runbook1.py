import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

def credential_test(task):
    task.run(task=send_command, command="show ip interface brief")

results = nr.run(task=credential_test)
print_result(results)
