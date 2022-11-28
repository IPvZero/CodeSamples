from napalm import get_network_driver 
from rich import print as rprint 

juniper_device = get_network_driver("junos")
with juniper_device(hostname="192.168.4.101", username="john", password="Juniper1") as conn:
    conn.load_replace_candidate(filename="R1.cfg")
    conn.commit_config(revert_in=60)
    print(conn.has_pending_commit())
    conn.commit_config()
    print(conn.has_pending_commit())
