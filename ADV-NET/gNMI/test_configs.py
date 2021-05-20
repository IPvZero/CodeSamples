arista_config = [
    (
     "/interfaces/interface[name=Loopback99]/config",
{

        "arista-intf-augments:load-interval": 300,
        "openconfig-interfaces:description": "Configured by IPvZero using gNMI!",
        "openconfig-interfaces:enabled": True,
        "openconfig-interfaces:loopback-mode": True,
        "openconfig-interfaces:name": "Loopback99",
        "openconfig-interfaces:type": "iana-if-type:softwareLoopback",
        "openconfig-vlan:tpid": "openconfig-vlan-types:TPID_0X8100"
      }

    )
]
