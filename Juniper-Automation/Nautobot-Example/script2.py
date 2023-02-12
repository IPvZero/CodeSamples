import requests
from rich import print as rprint

URL = "https://192.168.4.63/api/dcim/devices/"

headers = {"Authorization": "Token 6055fa3a1c732f44d470df6bbbbb54fffae51197"}

payload = {
    "name": "R3",
    "device_type": "ea0d1979-2303-49d7-bad8-8ce94f84603f",
    "device_role": "099be9e3-57d3-4299-8996-1b9f590727a6",
    "site": "7d50eb6f-fdec-49fc-b550-75383384cbac",
    "status": "active",
    "platform": "d42a351b-b05e-4ebb-a3d8-ef0909cee269",
}

response = requests.post(URL, headers=headers, verify=False, json=payload)
rprint(response)
