ages = {"John": 35, "Michelle": 18, "Dmitry": 28, "Laura": 45, "Carl": 32}

party_people = {k: v for (k, v) in ages.items() if v > 20}
print(party_people)
