import os
import subprocess
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure

nr = InitNornir(config_file="config.yaml")
CLEAR = "clear"
CLEAN = "rm -r configs-diff current-config"


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


CURRENT = "pyats learn ospf config --testbed-file testbed.yaml --output current-config"
os.system(CURRENT)
command = subprocess.run(
    ["pyats", "diff", "golden-config", "current-config", "--output", "configs-diff"],
    stdout=subprocess.PIPE,
)
STRING_COMMAND = str(command)
if "Diff can be found" in STRING_COMMAND:
    os.system(CLEAR)
    print("ALERT: POTENTIAL PROBLEM DETECTED")
    answer = input(
        "Would you like to reverse the current configs back to their golden state? <y/n>: "
    )
    if answer == "y":

        def main():
            os.system(CLEAN)
            os.system(CLEAR)
            nr.run(task=load_vars)
            replace_results = nr.run(task=replace_config)
            print_result(replace_results)

        if __name__ == "__main__":
            main()
else:
    os.system(CLEAN)
    os.system(CLEAR)
    print("No problems detected")
