from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="config.yaml")

def configure_stuff(task):
    template_to_load = task.run(task=template_file, template="ntp.j2", path="templates")
    configuration = template_to_load.result
    task.run(task=netconf_edit_config, target="candidate", config=configuration)
    task.run(task=netconf_commit)

results = nr.run(task=configure_stuff)
print_result(results)
