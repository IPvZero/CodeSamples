import json
from rich import print as rprint
from genie.testbed import load
from pyats.async_ import pcall

def get_ospf(dev_name, testbed_value):
    routing_table = testbed_value.parse("show ip route")
    pretty_routing = json.dumps(routing_table, indent=2)
    rprint(f"{dev_name}\n{pretty_routing}\n\n")
    return routing_table


testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_ospf, dev_name=testbed.devices.keys(), testbed_value=testbed.devices.values())
import ipdb
ipdb.set_trace()
