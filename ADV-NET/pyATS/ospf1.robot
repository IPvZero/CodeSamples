*** Settings ***
Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot
Library   genie.libs.robot.GenieRobot

*** Test Cases ***

Connect to device
    use genie testbed "testbed.yaml"
    connect to all devices

Verify OSPF Neighbors
    verify count "4" "ospf neighbors" on device "Spine1"
    verify count "4" "ospf neighbors" on device "Spine2"
    verify count "2" "ospf neighbors" on device "Leaf3"
    verify count "2" "ospf neighbors" on device "Leaf4"
    verify count "2" "ospf neighbors" on device "Leaf5"
    verify count "2" "ospf neighbors" on device "Leaf6"


Disconnect from device
    disconnect from all devices
