from fastapi import FastAPI, Request
from yaml import safe_load
from fastapi.templating import Jinja2Templates
from nornir_logic import get_running_devices
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command

nr = InitNornir(config_file="config.yaml")
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root() -> str:
    """Root page of the application

    Returns:
        str: A simple greeting message
    """
    return "Hello from CBT Nuggets"


@app.get("/inventory")
async def get_devices():
    return nr.inventory.hosts


@app.get("/all", tags=["variables"])
async def get_all_vars() -> dict:
    """Get all the variables within the ALL group

    Returns:
        dict: Dictionary of the variables within the YAML file
    """
    with open("group_vars/all.yaml", encoding="utf-8") as file:
        all_vars = safe_load(file)
    return {"all": all_vars}


@app.get("/devinfo", tags=["variables"])
async def get_all_info() -> dict:
    """Get all host information for the Nornir hosts.yaml file

    Returns:
        dict: Dictionary of the Nornir hosts
    """
    with open("hosts.yaml", encoding="utf-8") as file:
        info_data = safe_load(file)
    return {"info": info_data}


@app.get("/get-running")
async def get_running(request: Request):
    result = get_running_devices()
    return templates.TemplateResponse(
        "output.html", {"request": request, "output": result}
    )


@app.get("/get-running/{hostname}")
async def get_running_device(hostname):
    device = nr.filter(device_name=f"{hostname}")
    return device.run(netmiko_send_command, command_string="show configuration")
