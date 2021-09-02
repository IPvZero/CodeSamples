import yaml
from rich import print as rprint

def pull_yaml():
    """
    Function to pull yaml data
    """
    config_data = yaml.safe_load(open("R1.yaml"))
    bgp_stuff = config_data["BGP"]
    peers = bgp_stuff["peers"]
    for peer in peers:
        nbor = peer["neighbor"]
        asnumber = peer["peer_asn"]
        print(f"The neighbor {nbor} has an ASN of {asnumber}")

pull_yaml()
