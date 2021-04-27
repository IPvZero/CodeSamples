from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs_from_file
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

def push_tcam(task):
    task.run(task=send_configs_from_file, file="leaf-tcam.txt")

filtered = nr.filter(F(layer="Leaf"))
tcam_results = filtered.run(task=push_tcam)
print_result(tcam_results)
