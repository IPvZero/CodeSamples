import sys
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError


device = Device(host="192.168.4.101", user="john", passwd="Juniper1")
try:
    device.open()
except ConnectError as err:
    print("Device connection failed")
    sys.exit(1)
except Exception as err:
    print(err)
    sys.exit(1)

config = Config(device)
bgp_config = """
protocols {
    bgp {
        description THISISSOMEBGPSTUFF;
        local-as 65001;
    }
    ospf {
        area 0.0.0.0 {
            interface ge-0/0/0.0;
            interface ge-0/0/1.1;
        }
    }
}
"""
config.lock()
config.load(bgp_config)
config.pdiff()
if config.commit_check() == True:
    config.commit()
else:
    config.rollback()
config.unlock()
device.close()
