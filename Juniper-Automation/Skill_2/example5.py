import yaml
from rich import print as rprint

my_data = yaml.safe_load(open("hosts.yaml"))
bgp_neighbors = my_data["bgp"]["neighbors"]
for neighbor in bgp_neighbors:
    print(neighbor)
