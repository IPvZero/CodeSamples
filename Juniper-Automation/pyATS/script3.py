from pyats import aetest
from genie.testbed import load


class JunosTest(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)

    @aetest.test
    def get_version(self):
        for device in self.parameters["testbed"].devices.values():
            result = device.parse("show version")
            assert result["software-information"]["junos-version"] == "18.2R1.8"


testbed = load("testbed.yaml")
aetest.main(testbed=testbed)
