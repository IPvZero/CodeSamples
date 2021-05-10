"""
AUTHOR: IPvZero
"""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_scrapli.tasks import netconf_edit_config

nr = InitNornir(config_file="config.yaml")

def load_vars(task):
    """
    Load vars into memory
    """

    data = task.run(
        task=load_yaml,
        name="Loading Vars Into Memory...",
        file=f"./host_vars/{task.host}.yaml",
    )
    task.host["facts"] = data.result


def config_vpns(task):
    """
    Build Template and Push Config
    """
    vpn_template = task.run(
        task=template_file,
        name="Buildling VPN Configuration",
        template="combined.j2",
        path="./templates",
    )
    vpn_output = vpn_template.result

    task.run(
        task=netconf_edit_config,
        name="Automating MPLS L3 VPN",
        target="running",
        config=vpn_output,
    )

nr.run(task=load_vars)

vpn_results = nr.run(task=config_vpns, name="VPNS CONFIGURATION")
print_result(vpn_results)
