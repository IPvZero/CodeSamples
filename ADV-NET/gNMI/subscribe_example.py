from nornir import InitNornir
from pygnmi.client import gNMIclient, telemetryParser

nr = InitNornir(config_file="config.yaml")

subscribe = {
    'subscription': [
        {
            'path': 'openconfig-interfaces:interfaces',
            'mode': 'sample',
            'sample_interval': 1000000000
        }
    ],
    'mode': 'stream',
    'encoding': 'json'
        
}

def test(task):
    with gNMIclient(
        target=(task.host.hostname, task.host.port),
        username=task.host.username,
        password=task.host.password,
        insecure=True,
    ) as client:
        response = client.subscribe(subscribe=subscribe)
        for rsp in response:
            print(telemetryParser(rsp))

nr.run(task=test)
