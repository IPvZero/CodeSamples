from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs_from_file


nr = InitNornir(config_file="config.yaml")

def enable_features(task):
    task.run(task=send_configs_from_file, file="basepusher.txt")


results = nr.run(task=enable_features)
print_result(results)
