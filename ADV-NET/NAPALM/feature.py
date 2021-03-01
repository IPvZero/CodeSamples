"""
Author: IPvZero
"""


from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from ipvzero_tasks import replace_vrf

nr = InitNornir(config_file="config.yaml")


def replace_feature(task):

    config = replace_vrf(task)
    task.run(task=napalm_configure, configuration=config, replace=True)


result = nr.run(task=replace_feature)
print_result(result)
