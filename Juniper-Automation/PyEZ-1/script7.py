from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_pyez.plugins.tasks import (
    pyez_get_config,
    pyez_config,
    pyez_commit,
    pyez_int_terse,
)

nr = InitNornir(config_file="config.yaml")

snmp_config = """
snmp {
    community NORNIR1;
    community NORNIR2;

}
"""


def test_stuff(task):
    task.run(task=pyez_config, payload=snmp_config)
    task.run(task=pyez_commit)
    task.run(task=pyez_int_terse)


results = nr.run(task=test_stuff)
print_result(results)
