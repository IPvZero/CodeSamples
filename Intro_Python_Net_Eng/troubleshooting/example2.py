import logging
from scrapli.driver.core import IOSXEDriver

logging.basicConfig(filename="newlogsconfigs.txt", level=logging.DEBUG)

def test_func():
    with IOSXEDriver(
        host="192.168.31.101",
        auth_username="john",
        auth_password="cisco",
        auth_strict_key=False,
        ssh_config_file=True,
    ) as conn:
        response = conn.send_configs(["router ospf 51"])
        return response.result

if __name__ == "__main__":
    results = test_func()
    print(results)
