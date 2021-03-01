import logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_validate
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result

nr = InitNornir(config_file="config.yaml")

def validate_test(task):
    result = task.run(task=napalm_validate, src=f"validate-{task.host}.yaml", severity_level=logging.DEBUG)
    task.host["facts"] = result.result
    assessment = task.host["facts"]["complies"]
    if assessment == True:
        message = "PASS"
    else:
        message = task.host["facts"]
    return Result(host=task.host, result=message)

results = nr.run(task=validate_test)
print_result(results)
