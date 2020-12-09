"""
INSTALL THE FOLLOWING:

pip3 install nornir
pip3 install nornir-scrapli
pip3 install nornir_utils
"""

from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="reader.txt")

legend_or_tennis = nr.filter(F(legend=True) | F(location="court"))
results = legend_or_tennis.run(task=banner_push)
print_result(results)
