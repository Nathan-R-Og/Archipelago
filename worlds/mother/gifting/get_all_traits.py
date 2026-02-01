lines = open("worlds/mother/gifting/gift_tags.py", "r").readlines()

all_traits = []

import ast
reading = False
for line in lines:
    if line.startswith("gift_properties"):
        reading = True
        continue

    if not reading:
        continue

    if line.find("create_gift") == -1:
        continue

    s = line.split("create_gift")[-1].split(",", 2)[-1].replace("),", "").replace(")", "").strip()
    traits = ast.literal_eval(s)
    for trait in traits:
        if not trait in all_traits:
            all_traits.append(trait)

for trait in all_traits:
    print(trait)