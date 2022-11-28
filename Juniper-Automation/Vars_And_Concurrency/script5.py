"""Concurrency Test"""
from concurrent.futures import ThreadPoolExecutor
from inventory import DEVICES
from utils import load_vars, generate_config, configure_junos



def main(device):
    """Main function"""

    groups = device["groups"]
    hostname = device["hostname"]
    device_vars = load_vars(device, groups)
    configuration = generate_config(device_vars)
    configure_junos(hostname, configuration)


with ThreadPoolExecutor() as executor:
    results = executor.map(main, DEVICES)
