import requests

query = """
query {
  devices {
    name
  }
}
"""
payload = {"query": query}

url = "https://192.168.4.63/api/graphql/"

headers = {
    "Authorization": "Token 6055fa3a1c732f44d470df6bbbbb54fffae51197",
    "Content-Type": "application/json",
}

response = requests.post(url, headers=headers, json=payload, verify=False)

print(response.status_code)
print(response.json())
