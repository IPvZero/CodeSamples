import os
import logging
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

logger = logging.getLogger(__name__)

nr = InitNornir(config_file="config.yaml")


def push_snmp(task, filename):
    if not os.path.isfile(filename):
        logger.error(f"{filename} cannot be found")
    task.run(task=netmiko_send_config, config_file=filename)


north_junos_devices = nr.filter(
    latitude="north", platform="juniper_junos", state="north dakota"
)
results = north_junos_devices.run(task=push_snmp, filename="northconfig.cfg")
print_result(results)
