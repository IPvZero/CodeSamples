import sys

target = sys.argv[1]
etx = chr(3)

def get_config():
    with open(target, "r") as f:
        my_data = f.read()
        final_config = my_data.replace("^C", etx)
    return final_config


def update_config(result):
    with open(target, 'w') as q:
        q.write(result)

result = get_config()
update_config(result)
