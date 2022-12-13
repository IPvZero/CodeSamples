#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from scrapli import Scrapli


def connect_junos(device_ip):
    device = {
        "host": device_ip,
        "auth_username": "john",
        "auth_password": "Juniper1",
        "auth_strict_key": False,
        "platform": "juniper_junos"
    }
    conn = Scrapli(**device)
    conn.open()
    result = conn.send_command("show configuration")
    return result.result

def main():
    data_fields = {"ip": {}}

    module = AnsibleModule(argument_spec=data_fields)
    device_ip = module.params["ip"]
    result = connect_junos(device_ip)
    module.params.update({"result": result })
    module.params.pop("ip")
    module.exit_json(data=module.params)

if __name__ == "__main__":
    main()