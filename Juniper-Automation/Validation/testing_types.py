from platform import platform
import yaml
from jinja2 import Environment, FileSystemLoader
from scrapli import Scrapli
from scrapli.response import MultiResponse
from typing import List

from inv import DEVICES


def create_config(hostname: str) -> List[str]:
    """
    Function to gather YAML Data from host_vars
    and then return device Configs

    Args:
        hostname (str): Each hostname with the inv Inventory file

    Returns:
        List[str]: The device configuration line-by-line
    """

    yaml_data = yaml.safe_load(open(f"host_vars/{hostname}.yaml"))
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("config.j2")
    my_configs = template.render(yaml_data)
    configuration = my_configs.splitlines()
    return configuration


def send_configurations(host: str, configuration: List[str]) -> MultiResponse:
    """
    Function to send rendered configs to devices

    Args:
        host (str): The IP address for each device with the inv inventory file
        configuration (List[str]): The device configuration line-by-line

    Returns:
        MultiResponse: Scrapli's Multiresponse from the targeted device
    """
    with Scrapli(
        host=host,
        auth_username="john",
        auth_password="Juniper1",
        auth_strict_key=False,
        platform="juniper_junos",
    ) as conn:
        response = conn.send_configs(configs=configuration)
        return response


def main() -> None:
    for device in DEVICES:
        hostname = device["hostname"]
        host = device["host"]
        configuration = create_config(hostname)
        result = send_configurations(host, configuration)
        print(result.result)


main()
