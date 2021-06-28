from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")


def testplatform(task):
    print(f"{task.host.platform}-templates")


nr.run(task=testplatform)
