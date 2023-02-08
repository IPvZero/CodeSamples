from genie.testbed import load
from rich import print as rprint

testbed = load("testbed.yaml")


for device in testbed.devices.keys():
    device = testbed.devices[device]
    device.connect(log_stdout=False)
    ntp_config = device.learn("ntp")
    rprint(ntp_config.to_dict())
