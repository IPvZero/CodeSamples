import requests
from rich import print as rprint

query = """
query {
  devices {
    id
    name
    interfaces {
      name
      ip_addresses {
        address
      }
    }
  }
}
"""
payload = {"query": query}

URL = "https://192.168.4.63/api/graphql/"
headers = {
    "Authorization": "Token 6055fa3a1c732f44d470df6bbbbb54fffae51197",
    "Content-Type": "application/json",
}

response = requests.post(URL, headers=headers, json=payload, verify=False)
rprint(response.status_code)
dict_response = response.json()
devices = dict_response["data"]["devices"]
for device in devices:
    rprint(device)
