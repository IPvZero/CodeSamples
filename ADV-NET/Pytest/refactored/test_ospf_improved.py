"""
This script was written with help from Dmitry Figol
https://github.com/dmfigol/
"""


from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
import pytest
from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")


def check_ospf_neighbors_data_task(task):
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["ospf_neighbor_data"] = result.scrapli_response.genie_parse_output()

def get_spine_leaf_dev_names():
    devices = nr.filter(F(role="Spine") | F(role="Leaf")).inventory.hosts.keys()
    return devices


class TestOSPFNeighbors:
    NEIGHBOR_COUNT = {
        "Spine": 4,
        "Leaf": 2
    }

    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self, pytestnr):
        pytestnr_filtered = pytestnr.filter(F(role="Spine") | F(role="Leaf"))
        pytestnr_filtered.run(task=check_ospf_neighbors_data_task)
        yield
        for host in pytestnr_filtered.inventory.hosts.values():
            host.data.pop("ospf_neighbor_data")

    @pytest.mark.parametrize(
        'device_name', get_spine_leaf_dev_names()
        )

    def test_ospf_neighbor_count(self, pytestnr, device_name):
        my_list = []
        nr_host = pytestnr.inventory.hosts[device_name]
        role = nr_host["role"]
        interfaces = nr_host["ospf_neighbor_data"]["interfaces"]
        for interface in interfaces:
            ospf_neighbor = interfaces[interface]["neighbors"]
            for key in ospf_neighbor:
                my_list.append(key)
        num_neighbors = len(my_list)
        expected_neighbors = TestOSPFNeighbors.NEIGHBOR_COUNT[role]
        assert num_neighbors == expected_neighbors
