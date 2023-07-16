import json
test_dict = {}
names = ["sea1", "sea2", "sea3", "sea4", "sea5", "sea6", "sea7", "sea8", "water_rock", "sign1", "sign2", "encounter_grass", "bush1", "cut_tree", "strength_rock", "br_bush", "bush2", "flower", "water_rock2", "grass1", "grass2", "grass3", "grass4", "bush3", 'hor_fence1', 'hor_fence2', 'ver_fence1, ver_fence2', 'cor_fence1', 'tl_bush', 'hor_bush', 'tr_bush', 'bush4', 'ver_bush', 'bl_bush']
for i in range(2):
    for j in range(17):
        test_dict[names[j + 17 * i]] = {"frame": {"x": 4 + 17 * j, "y": 3 + 17 * i , "w": 16, "h": 16}, "rotated": False, "trimmed": False}
f = open("test.json", "w")
print(json.dumps(test_dict, indent = 4))
# print(test_dict)