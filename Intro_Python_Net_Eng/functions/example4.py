def device_login(username, hostname, platform="cisco"):
    print(f"ssh {username}@{hostname}")
    if platform == "cisco":
        print("enable\nconfigure terminal\n")
    elif platform == "junos":
        print("cli\nedit\n")

device_login("john", "192.168.1.1", "junos")

#This won't work - positional arg after keyword arg
device_login(username="john", "8.8.8.8", "cisco")
