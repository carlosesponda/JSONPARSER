import json
import re

_keys = "type filename line automatic_features".split()


class LimitedDict(dict):

    def __init__(self, valtype=int):
        for key in _keys:
            self[key] = valtype()
        self["tool"] = "Typechef-VAA"
        self["description"] = ""
        self["configs"] = []
        self["num_configs"] = "-1"
        self["variability"] = "true"
        self["target"] = "sqlite3"

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)


def processfeatures(str):
    str = str.replace('(','')
    str = str.replace(')', '')
    str = str.replace('!def', ' -')
    str = str.replace('def', ' ')
    str = str.replace('&', '')
    str = str.replace('|', '')
    return list(set(str.split()))


def processfilename(str):
    str = str.replace("_DEGREE_DETAIL", "")
    if str == "DEADSTORE":
        str="Dead store"
    elif str == "UNINITIALIZEDMEMORY":
        str= "Uninitialized memory"
    elif str == "CASETERMINATION":
        str = "Case termination"
    elif str == "CHECKSTDLIBFUNCRETURN":
        str = "Check stdlibfunc return"
    return str


def main():
    dicts = []
    d = LimitedDict()
    ks = _keys
    with open("parse.txt") as f:
        for line in f:
            line = line[:-1]
            line = line.replace("[","")
            line = line.replace("]"," ")
            line = line.replace("(","",1)
            line = line.replace(")"," ",1)
            line = line.replace(" @","")
            line = line.replace("file ","")
            line = line.lstrip()
            line = re.sub('/[^>]+/','',line)
            line = re.sub('case.*?:', '', line)
            line = line.replace(':',' ',1)
            line = line.replace(' \t'," ")
            line = line.replace('\t', " ")
            line = line.replace('\n','')
            val = line.split(" ",5)
            del val[1]
            i = 0
            while i < len(_keys):
                if i==0:
                    d[ks[i]] = processfilename(val[i])
                elif i==1:
                    d[ks[i]] = val[i]
                elif i==2:
                    str= val[i].split(':')
                    d[ks[i]] = str[0]
                elif i == 3:
                    d[ks[i]] = processfeatures(val[i])
                i += 1
            dicts.append(d)
            d = LimitedDict()

        print(json.dumps(dicts))


if __name__ == '__main__':
    main()








