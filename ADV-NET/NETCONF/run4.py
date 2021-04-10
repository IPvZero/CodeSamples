import xmltodict
from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get
from nornir_utils.plugins.functions import print_result
from pprint import pprint

nr = InitNornir(config_file="config.yaml")

def get_yang(task):
    result = task.run(task=netconf_get, filter_type="xpath", filter_="interfaces-state//statistics[in-unicast-pkts > 0]")
    output = result.result
    dict_result = xmltodict.parse(output)
    task.host["facts"] =dict_result
    interfaces = task.host["facts"]["rpc-reply"]["data"]["interfaces-state"]["interface"]
    for intf in interfaces:
        interface_name = intf["name"]
        print(f"{interface_name}'s in-unicast-ptks are greater than zero")

results = nr.run(task=get_yang)
#print_result(results)
#import ipdb
#ipdb.set_trace()
