from ncclient import manager


def connect():
    conn = manager.connect(
        host="192.168.4.102",
        port=830,
        username="john",
        password="Juniper1",
        timeout=30,
        device_params={"name": "junos"},
        hostkey_verify=False,
    )
    response = conn.get_config("running")
    print(response)


connect()
