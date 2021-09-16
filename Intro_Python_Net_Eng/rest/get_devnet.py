import json
import httpx
from rich import print as rprint

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
my_url = "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/native"


def pull_info(url):
    with httpx.Client(verify=False) as client:
        response = client.get(url, headers=headers, auth=("developer", "C1sco12345"))
        return response.text


results = pull_info(my_url)
rprint(results)
