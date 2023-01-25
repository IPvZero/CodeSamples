import json
import requests
from rich import print as rprint

BASE_URL = "http://192.168.4.101:8080/rpc"

endpoint = "/get-system-users-information"
credentials = ("john", "Juniper1")

headers = {"Accept": "application/json"}

try:
    response = requests.get(BASE_URL + endpoint, auth=credentials, headers=headers)
    dict_response = json.loads(response.text)
    rprint(dict_response["system-users-information"]["uptime-information"]["up-time"])

except requests.exceptions.RequestException as err:
    rprint(f"ERROR: {err}")

except Exception as e:
    rprint(f"ERROR: {e}")
