"""
Author: IPvZero
"""

import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print
from rich.console import Console
from rich.table import Table

nr = InitNornir(config_file='config.yaml')
failed_list = []

with open('reader.txt', 'r') as f:
    filelines = f.read().splitlines()

def ping_test(task):
    for target in filelines:
        result = task.run(send_command, command="ping " + target)
        response = result.result
        if not "!!!" in response:
            failed_list.append(f"{task.host} cannot ping {target}")

nr.run(task=ping_test)
if failed_list:
    sorted_list = sorted(failed_list)
    print(sorted_list)
else:
    print("All pings were successful")
