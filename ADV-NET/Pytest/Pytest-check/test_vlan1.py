from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from pytest_check import check_func

def load_vars(task):
    result = task.run(task=load_yaml, file=f"desired-state/vlans/{task.host}.yaml")
    loaded = result.result
    return loaded

@check_func
def get_vlans(task):
    vlan_list = []
    result = task.run(task=send_command, command="show vlan")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    vlans = task.host["facts"]["vlans"]
    for vlan in vlans:
        if vlan in ["1", "1002", "1003", "1004", "1005"]:
            continue
        vlan_id = int(vlan)
        name = vlans[vlan]["name"]
        vlan_dict = {"id": vlan_id, "name": name}
        vlan_list.append(vlan_dict)
    expected = load_vars(task)["vlans"]
    assert expected == vlan_list, f"{task.host} FAILED"

def test_nornir(nr):
    nr.run(task=get_vlans)
