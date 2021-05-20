from pygnmi.client import gNMIclient
from test_configs import arista_config
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")

def test(task):
    with gNMIclient(
        target=(task.host.hostname, task.host.port),
        username=task.host.username,
        password=task.host.password,
        insecure=True,
    ) as client:
        client.set(update=arista_config)

nr.run(task=test)
