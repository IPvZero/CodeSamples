import json
import httpx
from rich import print as rprint

headers = {
    "Authorization": "Bearer 0470438c7d610c609bb45121cdcdbf152eed82f073228fcbef45809942d46068",
}
my_url = "https://gorest.co.in/public/v1/users"

payload = {
    "name": "Trevor Sullivan",
    "gender": "male",
    "email": "trevorsullivan17823872@15ce.com",
    "status": "active",
}


def post_stuff(url):
    with httpx.Client() as client:
        response = client.post(url, headers=headers, data=payload)
        structured_response = json.loads(response.text)
        return response, structured_response


results = post_stuff(url=my_url)
rprint(results)
