from pyats import aetest
from genie.testbed import load


class JunosTest(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)

    @aetest.test
    def get_product_name(self):
        for device in self.parameters["testbed"].devices.values():
            result = device.parse("show version")
            assert result["software-information"]["product-name"] == "ios"


testbed = load("testbed.yaml")
aetest.main(testbed=testbed)
