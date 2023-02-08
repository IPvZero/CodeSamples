import json
from webbrowser import get
from netmiko import ConnectHandler
import pytest


@pytest.fixture()
def get_communities():
    conn = ConnectHandler(
        device_type="juniper_junos",
        ip="192.168.4.101",
        username="john",
        password="Juniper1",
    )
    result = conn.send_command(command_string="show configuration snmp | display json")
    dict_result = json.loads(result)
    communities = dict_result["configuration"]["snmp"]["community"]
    return communities


def test_length(get_communities):
    for community in get_communities:
        community_name = community["name"]
        assert (
            1 <= len(community_name) <= 2
        ), f"Community {community_name} is not between 5 and 9 characters"


def test_digits(get_communities):
    for community in get_communities:
        community_name = community["name"]
        for character in community_name:
            if character.isdigit():
                assert False, f"Community {community_name} contains a digit"
