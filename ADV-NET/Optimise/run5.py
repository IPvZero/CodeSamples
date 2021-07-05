from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def enable_scp(task):
    task.run(task=send_config, config="ip scp server enable")


results = nr.run(task=enable_scp)
print_result(results)
