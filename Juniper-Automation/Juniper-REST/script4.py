import json
import httpx
from rich import print as rprint

BASE_URL = "http://192.168.4.101:8080/rpc"
endpoint = "/get-snmp-v3-information"

credentials = ("john", "Juniper1")
headers = {"Accept": "application/json"}

try:
    with httpx.Client() as client:
        response = client.post(BASE_URL + endpoint, auth=credentials, headers=headers)
        response.raise_for_status()
        rprint(json.loads(response.text))

except httpx.HTTPError as h_err:
    print(f"HTTP ERROR: {h_err}")
except httpx.ConnectTimeout as t_err:
    print(f"TIMEOUT ERROR: {t_err}")
except Exception as e:
    print("ERROR: {e}")
