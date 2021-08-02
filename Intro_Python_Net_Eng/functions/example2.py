my_list = [1, 2, 3, [2, 2, 5], 6, 45, 78]
for num in my_list:
    if isinstance(num, list):
        for n in num:
            if n == 5:
                print("The number 5 is present")
    else:
        if num == 5:
            print("The number 5 is present")
 
