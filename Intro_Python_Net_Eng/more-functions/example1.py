interface_list = ["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2", "Loopback0", "Loopback1"]

#gig_list = []
#
#for interface in interface_list:
#    if interface.startswith("Gig"):
#        gig_list.append(interface)
#
#print(gig_list)

gig_list = [interface for interface in interface_list if interface.startswith("Gig")]
print(gig_list)
