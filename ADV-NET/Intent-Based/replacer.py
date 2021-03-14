from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure

nr = InitNornir(config_file="config.yaml")


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result


def replace_config(task):
    template_results = task.run(
        task=template_file, template=f"{task.host}.j2", path="./templates"
    )
    task.host["base_config"] = template_results.result
    configuration = task.host["base_config"]
    task.run(task=napalm_configure, configuration=configuration, replace=True)


loaded_results = nr.run(task=load_vars)
replace_results = nr.run(task=replace_config)
print_result(loaded_results)
print_result(replace_results)
