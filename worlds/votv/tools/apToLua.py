from worlds.votv.data.item_data import shop_items
from worlds.votv.Locations import location_table
from worlds.votv.Items import item_table
from worlds.votv.Types import BASE_ID, LOC_OFFSET, ITEM_OFFSET

#shop codes
lines = [
"item_map = {\n"
]

for item in shop_items.keys():
    item_normal = item.replace("\"", "\\\"")
    newline = f'["{shop_items[item].internal_name}"] = \"{item_normal}\",\n'
    lines.append(newline)

lines.append("}\n")

open("item_map.lua", "w").writelines(lines)

#locations
lines = [
f"BASE_ID = {hex(BASE_ID)}\n"
f"LOC_OFFSET = {hex(LOC_OFFSET)}\n"
"\n"
"locations = {\n"
]

print('s')

for location in location_table.keys():
    location_code = location_table[location].base_code
    location_normal = location.replace("\"", "\\\"")
    newline = f'[\"{location_normal}\"] = {location_code} + BASE_ID + LOC_OFFSET,\n'
    lines.append(newline)

lines.append("}\n")

open("locations.lua", "w").writelines(lines)

#items
lines = [
f"BASE_ID = {hex(BASE_ID)}\n"
f"ITEM_OFFSET = {hex(ITEM_OFFSET)}\n"
"\n"
"items = {\n"
]

print('s')

for item in item_table.keys():
    item_code = item_table[item].base_code
    item_name_normal = item.replace("\"", "\\\"")
    newline = f'[\"{item_name_normal}\"] = {item_code} + BASE_ID + ITEM_OFFSET,\n'
    lines.append(newline)

lines.append("}\n")

open("items.lua", "w").writelines(lines)