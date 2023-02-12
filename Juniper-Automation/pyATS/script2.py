from genie.testbed import load
from pyats.async_ import pcall
from rich import print as rprint


def get_ntp_test(dev):
    ntp_config = dev.learn("ntp")
    rprint(ntp_config.to_dict())


testbed = load("testbed.yaml")
testbed.connect(log_stdout=False)
results = pcall(get_ntp_test, dev=testbed.devices.values())
