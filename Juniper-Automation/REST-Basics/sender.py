import requests
from rich import print as rprint

BASE_URL = "http://192.168.4.63:5050"


def get_networks():
    response = requests.get(f"{BASE_URL}/networks")
    return response.json()


def get_network(id):
    response = requests.get(f"{BASE_URL}/network/{id}")
    if response.status_code == 404:
        raise ValueError(response.json()["error"])
    return response.json()


def create_network(name, subnets):
    data = {"name": name, "subnets": subnets}
    response = requests.post(f"{BASE_URL}/network", json=data)
    if response.status_code == 400:
        raise ValueError(response.json()["error"])
    return response.json()


def update_network(id, name, subnets):
    data = {"name": name, "subnets": subnets}
    response = requests.put(f"{BASE_URL}/network/{id}", json=data)
    if response.status_code == 404 or response.status_code == 400:
        raise ValueError(response.json()["error"])
    return response.json()


def delete_network(id):
    response = requests.delete(f"{BASE_URL}/network/{id}")
    if response.status_code == 404:
        raise ValueError(response.json()["error"])
    return response.json()


def main():
    while True:
        answer = input(
            "Which function would you like to use? [get_networks, get_network, create_network, update_network, delete_network]. Please type 'exit' to exit the program: "
        )
        if answer == "get_networks":
            rprint(get_networks())
        elif answer == "get_network":
            id = input("Enter the network ID you wish to target: ")
            rprint(get_network(id))
        elif answer == "create_network":
            name = input("Enter the name of the network you want to create: ")
            subnet_list = input(
                "Enter the subnets you want to add (separated by commas): "
            )
            subnets = subnet_list.split(",")
            rprint(create_network(name, subnets))
        elif answer == "update_network":
            id = input("Enter the network ID you wish to target: ")
            name = input("Enter the name of the network you want to create: ")
            subnet_list = input(
                "Enter the subnets you want to add (separated by commas): "
            )
            subnets = subnet_list.split(",")
            rprint(update_network(id, name, subnets))
        elif answer == "delete_network":
            id = input("Enter the network ID you wish to target: ")
            rprint(delete_network(id))
        elif answer == "exit":
            break
        else:
            print("That input is invalid")


if __name__ == "__main__":
    main()
