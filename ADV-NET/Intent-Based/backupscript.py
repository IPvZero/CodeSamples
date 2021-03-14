import pathlib
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir(config_file="config.yaml")

config_directory = "backups"


def backup_config(task):
    config_result = task.run(task=napalm_get, getters=["config"])
    running_config = config_result.result["config"]["running"]
    pathlib.Path(config_directory).mkdir(exist_ok=True)
    task.run(
        task=write_file, content=running_config, filename=f"backups/{task.host}.txt"
    )


results = nr.run(task=backup_config)
print_result(results)
