import os
import time
import itertools
import ipaddress
from subprocess import Popen, DEVNULL
from rich import print
from rich.console import Console
from rich.table import Table

CLEAR = "clear"
os.system(CLEAR)
localtime = time.asctime(time.localtime(time.time()))
active_list = []
inactive_list = []
p = {}


print("[green]Welcome to Linux Pinger![/green]")
print("[cyan]Please enter the network you wish to test...[/cyan]")
print("Example: < 192.168.10.0/24 >")
subnet = input("\nEnter network: ")
print("\n")
network = ipaddress.ip_network(subnet)

for n in network.hosts():
    IP = str(n)
    p[IP] = Popen(['ping', '-c', '4', '-i', '0.2', IP], stdout=DEVNULL)

while p:
    for IP, proc in p.items():
        if proc.poll() is not None:
            del p[IP]
            if proc.returncode == 0:
                active_list.append(IP)
            elif proc.returncode == 1:
                inactive_list.append(IP)
            else:
                print(f"{IP} ERROR")
            break

table = Table(title="PING REPORT \n" + localtime)
table.add_column("Active Hosts", justify="center", style="green")
table.add_column("Inactive Hosts", justify="center", style="red")
for (a, i) in itertools.zip_longest(active_list, inactive_list):
    table.add_row(a, i)
console = Console()
console.print(table)
