from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def configure_some_data(task):
    task.run(task=napalm_configure, configuration="set snmp community NAPALMTEST")


result = nr.run(task=configure_some_data)
print_result(result)
