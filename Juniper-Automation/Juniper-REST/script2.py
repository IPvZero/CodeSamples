import json
from rich import print as rprint
import requests

BASE_URL = "http://192.168.4.101:8080/rpc"

endpoint = "/get-interface-information"
credentials = ("john", "Juniper1")

headers = {"Accept": "application/json"}
response = requests.post(BASE_URL + endpoint, auth=credentials, headers=headers)
rprint(response.text)
