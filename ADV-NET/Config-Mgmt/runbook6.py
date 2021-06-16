from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def send_configs_test(task):
    task.run(task=send_configs, configs=["router ospf 44", "network 0.0.0.0 255.255.255.255 area 44"])


results = nr.run(task=send_configs_test)
print_result(results)
