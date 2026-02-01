from rom_data import rom_item_table

lines = open("worlds/mother/Locations.py", "r").readlines()

def represents_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

items = {}

writing = False
i = 0
x = 0
while i < len(lines):
    line = lines[i]
    if line == "mother_locations = {\n":
        writing = True

    if line.find("OBJ_PICK_ITEM") != -1:
        objectn, command, item = line.split(" - ")
        command = command.replace("OBJ_PICK_ITEM ", "")
        id = 0
        if command.find("$") != -1:
            id = int(command.replace("$", "0x"), 16)
        else:
            id = int(command)
        command = hex(id)
        item = list(rom_item_table.keys())[id]

        if item in list(items.keys()):
            items[item] += 1
        else:
            items[item] = 1

        new_line = " - ".join([objectn, command, item])+"\n"
        lines[i] = new_line
    if line.find("OBJ_DISPLAY_ITEMS") != -1:
        objectn, command = line.split(" - ")
        command = command.replace("OBJ_DISPLAY_ITEMS ", "")
        ids = command.split(",")
        names = []
        for get_id in ids:
            id = 0
            if get_id.find("$") != -1:
                id = int(get_id.replace("$", "0x"), 16)
            else:
                id = int(get_id)
            if id >= 0x80:
                names.append(f"\t#{id}\n")
            else:
                itemname = list(rom_item_table.keys())[id]

                if itemname in list(items.keys()):
                    items[itemname] += 1
                else:
                    items[itemname] = 1

                names.append("\t#"+itemname+"\n")

        new_line = objectn+"\n"
        lines[i] = new_line
        i += 1
        names.reverse()
        for x in range(4):
            lines.insert(i, names[x])
        i += 3
    if line.find("#OBJ_") != -1 and line.find("PRESENT") != -1:
        objectn, item = line.split(" - ")
        id = 0
        if item.find("$") != -1:
            id = int(item.replace("$", "0x"), 16)
        elif represents_int(item):
            id = int(item)
        item = list(rom_item_table.keys())[id]

        if item in list(items.keys()):
            items[item] += 1
        else:
            items[item] = 1

        new_line = " - ".join([objectn, item])+"\n"
        lines[i] = new_line

    i += 1

open("worlds/mother/Locations_test.py", "w").writelines(lines)

for key in list(items.keys()):
    print(f"{key}: {items[key]}")