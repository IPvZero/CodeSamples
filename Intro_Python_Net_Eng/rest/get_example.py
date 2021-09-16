import json
import httpx
from rich import print as rprint

headers = {"Accept": "application/json", "Content-Type": "application/json"}
my_url = "https://gorest.co.in/public/v1/users"


def pull_info(url):
    with httpx.Client() as client:
        response = json.loads(client.get(url, headers=headers).text)
        return response


results = pull_info(my_url)
rprint(results["data"])
