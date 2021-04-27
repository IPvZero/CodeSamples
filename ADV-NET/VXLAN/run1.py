import logging
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml


nr = InitNornir(config_file="config.yaml")


def load_vars(task):
    loader = task.run(task=load_yaml, file=f"host_vars/{task.host}.yaml")
    group_loader = task.run(task=load_yaml, file="group_vars/all.yaml")
    task.host["facts"] = loader.result
    task.host["group_facts"] = group_loader.result



def vxlan_configs(task):
    template = task.run(
        task=template_file,
        template=f"{task.host['layer']}.j2",
        path="templates/vxlan",
        severity_level=logging.DEBUG,
    )
    task.host["vxlan_config"] = template.result
    rendered = task.host["vxlan_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)


nr.run(task=load_vars)
vxlan_results = nr.run(task=vxlan_configs)
print_result(vxlan_results)
