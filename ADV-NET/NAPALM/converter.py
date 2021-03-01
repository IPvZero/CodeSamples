import yaml
from pprint import pprint

target_dict = { 'get_facts': { 'fqdn': 'R1.cisco.com',
                 'hostname': 'R1',
                 'interface_list': [ 'GigabitEthernet0/0',
                                     'GigabitEthernet0/1',
                                     'GigabitEthernet0/2',
                                     'GigabitEthernet0/3',
                                     'GigabitEthernet0/4',
                                     'GigabitEthernet0/5',
                                     'GigabitEthernet0/6',
                                     'GigabitEthernet0/7',
                                     'Loopback0'],
                 'model': 'IOSv',
                 'os_version': 'IOSv Software (VIOS-ADVENTERPRISEK9-M), '
                               'Version 15.8(3)M2, RELEASE SOFTWARE (fc2)',
                 'serial_number': '94VRU9VO25TWFPNPT5VND',
                 'uptime': 4140,
                 'vendor': 'Cisco'}}

filename = "validate-R1.yaml"
with open(filename, "w") as f:
    output = yaml.dump(target_dict, f, default_flow_style=False)
