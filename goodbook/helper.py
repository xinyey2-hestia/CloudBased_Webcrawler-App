
import json
import collections

def storejson(data, filename):
    with open(filename + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

def loadjson(filename):
    with open(filename, 'rb') as file:
        return json.load(file)

def jsonParse(dir_data):
    data=loadjson(dir_data)
    actj=[]
    movj=[]
    for i in data[0].keys():
        actj.append(data[0][i])
    for i in data[1].keys():
        movj.append(data[1][i])
    return actj,movj