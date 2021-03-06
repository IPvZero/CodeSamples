import pytest
from nornir import InitNornir
@pytest.fixture(scope="session", autouse=True)
def nr():
    nr = InitNornir(config_file="config.yaml")
    yield nr
    nr.close_connections()
