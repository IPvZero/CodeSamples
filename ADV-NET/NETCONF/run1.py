from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

filt = """
 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      </name>
    </interface>
 </interfaces>
 """


def get_device_config(task):
    task.run(task=netconf_get_config, source="running", filter_type="subtree", filters=filt)

results = nr.run(task=get_device_config)
