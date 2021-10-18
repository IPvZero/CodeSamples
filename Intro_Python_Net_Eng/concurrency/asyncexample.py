import asyncio
from time import perf_counter
from scrapli.driver.core import AsyncIOSXEDriver
from rich import print as rprint
from inv import DEVICES

start = perf_counter()


async def get_dev_info(device):
    hostname = device["hostname"]
    async with AsyncIOSXEDriver(
        host=device["host"],
        auth_username="john",
        auth_password="cisco",
        auth_strict_key=False,
        ssh_config_file=True,
        transport="asyncssh",
    ) as conn:
        response = await conn.send_command("show version")
        return hostname, response.result


async def main():
    coroutines = [get_dev_info(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        rprint(f"[green]==={result[0]}===[/green]\n{result[1]}\n\n")


if __name__ == "__main__":
    asyncio.run(main())
