import json
import string

data = json.load(open("Black_Mirror.json"))

def getkey(data,k):
    for kin in data:
        if kin == k:
            return kin
    return None

def query_pars(data,query_str):
    r = query_str.split('/');
    root = data
    for kk in r:
        key_ = getkey(root,kk)
        if key_ == None:
            return False
        root = root[key_]
    return root

query_str = "LostFilm/season_1/part_1"
obg = query_pars(data,query_str)
obg['flag'] = '123'

with open('Black_Mirror_.json', 'w',encoding="utf-8") as json_file:
    json.dump(data, json_file)