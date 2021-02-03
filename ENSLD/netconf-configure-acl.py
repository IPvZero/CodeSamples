"""

Before running this script you must pip install the Scrapli-Netconf library:
python3 -m pip install scrapli-netconf

"""
from scrapli_netconf.driver import NetconfScrape

device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
    "port": 830,
}


configuration = """
  <config>
    <acl operation="replace" xmlns="http://openconfig.net/yang/acl">
      <acl-sets>
        <acl-set>
          <name>TEST2</name>
          <type>ACL_IPV4</type>
          <config>
            <name>TEST2</name>
            <type>ACL_IPV4</type>
          </config>
          <acl-entries>
            <acl-entry>
              <sequence-id>10</sequence-id>
              <config>
                <sequence-id>10</sequence-id>
              </config>
              <ipv4>
                <config>
                  <source-address>192.168.66.0/24</source-address>
                  <protocol xmlns:oc-acl-cisco="http://cisco.com/ns/yang/cisco-xe-openconfig-acl-ext">oc-acl-cisco:IP</protocol>
                </config>
              </ipv4>
              <transport>
                <config>
                  <source-port>ANY</source-port>
                  <destination-port>ANY</destination-port>
                </config>
              </transport>
              <actions>
                <config>
                  <forwarding-action>DROP</forwarding-action>
                  <log-action>LOG_NONE</log-action>
                </config>
              </actions>
            </acl-entry>
            <acl-entry>
              <sequence-id>20</sequence-id>
              <config>
                <sequence-id>20</sequence-id>
              </config>
              <ipv4>
                <config>
                  <source-address>10.10.20.0/24</source-address>
                  <protocol xmlns:oc-acl-cisco="http://cisco.com/ns/yang/cisco-xe-openconfig-acl-ext">oc-acl-cisco:IP</protocol>
                </config>
              </ipv4>
              <transport>
                <config>
                  <source-port>ANY</source-port>
                  <destination-port>ANY</destination-port>
                </config>
              </transport>
              <actions>
                <config>
                  <forwarding-action>DROP</forwarding-action>
                  <log-action>LOG_NONE</log-action>
                </config>
              </actions>
            </acl-entry>
            <acl-entry>
              <sequence-id>30</sequence-id>
              <config>
                <sequence-id>30</sequence-id>
              </config>
              <ipv4>
                <config>
                  <protocol xmlns:oc-acl-cisco="http://cisco.com/ns/yang/cisco-xe-openconfig-acl-ext">oc-acl-cisco:IP</protocol>
                </config>
              </ipv4>
              <transport>
                <config>
                  <source-port>ANY</source-port>
                  <destination-port>ANY</destination-port>
                </config>
              </transport>
              <actions>
                <config>
                  <forwarding-action>ACCEPT</forwarding-action>
                  <log-action>LOG_NONE</log-action>
                </config>
              </actions>
            </acl-entry>
          </acl-entries>
        </acl-set>
      </acl-sets>
    </acl>
  </config>
"""

connection = NetconfScrape(**device)
connection.open()
response = connection.edit_config(config=configuration, target="running")
print(response.result)
