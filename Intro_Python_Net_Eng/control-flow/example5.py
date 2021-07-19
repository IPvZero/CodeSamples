device_list = ["G0/0", "G0/1", "G0/2", "G0/3", "Loopback0", "Loopback1"]

#for device in device_list:
#    if device == "G0/2":
#        continue
#    print(device)

for device in device_list:
    if device.startswith("Loop"):
        continue
    print(device)
