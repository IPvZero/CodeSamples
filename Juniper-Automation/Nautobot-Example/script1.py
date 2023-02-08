import requests
from rich import print as rprint

URL = "https://192.168.4.63/api/dcim/devices/"

headers = {"Authorization": "Token 6055fa3a1c732f44d470df6bbbbb54fffae51197"}

response = requests.get(URL, headers=headers, verify=False)
rprint(response)
rprint(response.json())
