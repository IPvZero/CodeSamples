from pyats.async_ import pcall
from genie.testbed import load
from genie.utils import Dq
from rich import print as rprint

def get_ospf_routes(hostname, dev):
    parsed = dev.parse("show interfaces")
    oper_up = parsed.q.contains_key_value('oper_status', 'up').get_values('[0]', 0)
    rprint(oper_up)


testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_ospf_routes, hostname=testbed.devices.keys(), dev=testbed.devices.values())
