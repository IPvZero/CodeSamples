def test_func(device, command):
    print(f"sending {command} to {device}")

breakpoint()
test_func("R1", "show run")
