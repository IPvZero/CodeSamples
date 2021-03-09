*** Settings ***
Library   ats.robot.pyATSRobot
Library   unicon.robot.UniconRobot

*** Test Cases ***

Connect to device
    use testbed "testbed.yaml"
    connect to all devices

Execute NTP Commands
    configure "ntp server 77.77.77.77" on devices "Spine1"

Disconnect from device
    disconnect from all devices
