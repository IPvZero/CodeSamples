import json
import requests

from rich import print as rprint

requests.packages.urllib3.disable_warnings()


def get_token():
    token_url = "https://10.10.20.65/api/fdm/v5/fdm/token"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"grant_type": "password", "username": "admin", "password": "Cisco1234"}

    token_response = requests.post(
        token_url, headers=headers, data=json.dumps(payload), verify=False
    )
    token_response.raise_for_status()
    if token_response.status_code == 200:
        rprint("Token Received...\n")

    token = token_response.json()["access_token"]
    return token


def create_network(token):
    network_url = "https://10.10.20.65/api/fdm/v5/object/networks"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "name": "CBTN1",
        "description": "NUGGETS",
        "subType": "NETWORK",
        "value": "99.88.77.0/24",
        "dnsResolution": "IPV4_ONLY",
        "type": "networkobject",
    }

    create_response = requests.post(
        network_url, headers=headers, data=json.dumps(payload), verify=False
    )
    create_response.raise_for_status()
    if create_response.status_code == 200:
        rprint("[green]SUCCESS[/green]: New Object Created")
        rprint(create_response.text)


if __name__ == "__main__":
    token = get_token()
    create_network(token=token)
