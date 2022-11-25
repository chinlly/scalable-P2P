# import p2p_pi1
import json
import re
import Router
from os import read

# import requests

# for i in range(len(p2p_pi2.device_name)):
#    print(globals()[p2p_pi2.device_name[i]].router.getFib())
# import p2p_pi2

# print(p2p_pi1.names[p2p_pi1.device_name[0]].router.getFib())


line = '/diver/diver2/temperature'
pattern = r'/diver/diver2/position'
matchObj = re.match(pattern, line)
# print(matchObj.re)
# print(matchObj.re.pattern)
#
# print(line.split('/')[0:2])
# oop_len = 1 if 3 > 2 else 2
# print(oop_len)

# a = list(tuple())
# a.append((1, 2, 3))
# a.append((1, 2, 3))
# print(a)



# # get open source data
# response = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=9497ee3bc3b8486ebddcf1d6fc4bd67c")
# openData = response.json()["articles"][9]
# print(openData)

#
# with open("interfaces.json", 'r') as load_f:
#     load_dict = json.load(load_f)

# for i in range(len(load_dict)):
#     print(load_dict[i])
#     print(list(load_dict[i].keys())[0])
#     print(load_dict[list(load_dict[i].keys())[0]])

# print(load_dict)

# print(load_dict[0])
# device_name = list(load_dict[0].keys())[0]
# print(device_name)
# neighbour = load_dict[0][device_name][0]
# print(list(neighbour.keys())[0])
# print(neighbour[list(neighbour.keys())[0]])
# # print(load_dict.values(load_dict[0].keys()))
# print(type(neighbour[list(neighbour.keys())[0]]))


router = Router.Router('/divers/diver1')
print(router.getFib())

