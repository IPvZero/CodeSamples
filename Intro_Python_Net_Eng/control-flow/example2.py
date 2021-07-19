intf_list = ["interface g0/0", "interface g0/1", "interface g0/2", "interface loopback0"]

for interface in intf_list:
    print(f"{interface}\n ip ospf 1 area 0\n")
