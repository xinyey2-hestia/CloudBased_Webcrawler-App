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
    print(data['authors'])
    bookj=[]
    authorj=[]
    for i in data['books']:
        bookj.append(i)

    for i in data['authors']:
        authorj.append(i)

    return bookj,authorj

def get_key(key):
    try:
        return float(key)
    except ValueError:
        return key