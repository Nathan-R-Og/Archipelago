lines = open("worlds/mother/Locations.py", "r").readlines()

writing = False
i = 0
x = 0
for line in lines:
    if line == "mother_locations = {\n":
        writing = True

    if line.find("LocData(") == -1:
        continue

    new_line = line
    args = new_line.split("(", 1)[-1]
    new_args = args.split(",")
    new_args[0] = str(x)
    new_args = ",".join(new_args)
    x += 1
    new_line = line.replace(args, new_args)
    lines[lines.index(line)] = new_line

open("worlds/mother/Locations_test.py", "w").writelines(lines)

