from multiprocessing import Process
from time import sleep, perf_counter
from scrapli.driver.core import IOSXEDriver
from inv import DEVICES

start = perf_counter()

processes = []


def send_cmd(device):
    with IOSXEDriver(
        host=device["host"],
        auth_username="john",
        auth_password="cisco",
        auth_strict_key=False,
        ssh_config_file=True,
    ) as conn:
        response = conn.send_command("show version")
        print(response.result)


if __name__ == "__main__":
    for device in DEVICES:
        proc = Process(target=send_cmd, args=(device,))
        processes.append(proc)

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    end = perf_counter()
    total_time = end - start
    print(total_time)
