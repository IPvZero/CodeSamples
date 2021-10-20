def name_printer(name: str, uppercase: bool = False) -> None:
    if uppercase == True:
        print(name.upper())
    else:
        print(name)

name_printer("john", uppercase=True)
