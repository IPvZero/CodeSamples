with open("nested-file.txt") as f:
    my_data = f.readlines()
    for line in my_data:
        print(line)
