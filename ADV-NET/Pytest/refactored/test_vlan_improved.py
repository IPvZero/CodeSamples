"""
This script was written with help and guidance from Dmitry Figol
https://github.com/dmfigol/
"""

from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
import pytest
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")

def get_vlans(task):
    vlan_list = []
    result = task.run(task=send_command, command="show vlan")
    task.host["vlan_data"] = result.scrapli_response.genie_parse_output()


def load_vars(task):
    result = task.run(task=load_yaml, file=f"desired-state/vlans/{task.host}.yaml")
    task.host["loaded_vars"] = result.result

def get_dev_names():
    devices = (nr.inventory.hosts.keys())
    return devices

class TestVLANs:
    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self, pytestnr):
        pytestnr.run(load_vars)
        pytestnr.run(get_vlans)
        yield
        for host in pytestnr.inventory.hosts.values():
            host.data.pop("vlan_data")

    @pytest.mark.parametrize("device_name", get_dev_names())
    def test_vlans_for_consistency(self, pytestnr, device_name):
        vlan_list = []
        nr_host = pytestnr.inventory.hosts[device_name]
        expected_vlans = nr_host["loaded_vars"]["vlans"]
        vlans = nr_host["vlan_data"]["vlans"]
        for vlan in vlans:
            if vlan in ["1", "1002", "1003", "1004", "1005"]:
                continue
            vlan_id = int(vlan)
            name = vlans[vlan]["name"]
            vlan_dict = {"id": vlan_id, "name": name}
            vlan_list.append(vlan_dict)
        assert expected_vlans == vlan_list, f"{nr_host} FAILED"

