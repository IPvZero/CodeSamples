from scrapli.driver.core import IOSXEDriver
from inv import DEVICES


def find_macs(structured_result):
    my_mac = []
    for interface in structured_result:
        try:
            my_mac.append(structured_result[interface]["mac_address"])
        except KeyError:
            pass
    return my_mac

def send_cmd(device):
    with IOSXEDriver(
        host=device["host"],
        auth_username="john",
        auth_password="cisco",
        auth_strict_key=False,
        ssh_config_file=True,
    ) as conn:
        response = conn.send_command("show interfaces")
        structured_result = response.genie_parse_output()
        return structured_result

if __name__ == "__main__":
    for device in DEVICES:
        result = send_cmd(device)
        my_macs = find_macs(result)
        print(device)
        print(my_macs)
