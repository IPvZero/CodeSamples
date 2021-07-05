import os
from nornir import InitNornir
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = os.environ["USERNAME"]
nr.inventory.defaults.password = os.environ["PASSWORD"]

def randomtest(task):
    rprint(f"My name is {task.host}")
    rprint(f"My password is {task.host.password}")
    rprint(f"My username is {task.host.username}")
    rprint(f"My IP address is {task.host.hostname}")
    rprint(f"My platform is {task.host.platform}")
    rprint(f"My data is {task.host.data}")

nr.run(task=randomtest)
