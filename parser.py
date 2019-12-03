import json
import sys
import re

_keys = "type filename line automatic_features".split()

"""
How to use:

The python file first argument will always be the target. The rest are the files
that need to be parsed. If there are multiple files to process it is best to do the command:

"find -name "*vaa_detailreport" | parallel --xargs python parser.py "

"""

class jsonObject(dict):
    """

    A class used to create a dictionary with keys already defined.
    Each key is a json element that will be used to printed out.
    There are 10 keys in the dictionary.

    1. type
    2. filename
    3. line
    4. automatic_features
    5. tool
    6. description
    7. configs
    8. num_configs
    9. variability
    10. target

    the first four have to be parsed from the results of the tool
    the other 6 are predefined.

    """

    def __init__ (self, valtype=int):
        for key in _keys:
            self[key] = valtype()
        self["tool"] = "Typechef-VAA"
        self["description"] = ""
        self["configs"] = []
        self["num_configs"] = "-1"
        self["variability"] = "true"
        self["target"] = sys.argv[1]

    def __setitem__ (self, key, val):
        dict.__setitem__(self, key, val)


def processfeatures (str):
    """
    this function is to be able to process any of the automatic features that may be a result
    of Typechef. The output would usually be in paranthese and then describle the features with a def

    EX:

    """
    str = str.replace('(', '')
    str = str.replace(')', '')
    str = str.replace('!def', ' -')
    str = str.replace('def', ' ')
    str = str.replace('&', '')
    str = str.replace('|', '')
    return list(set(str.split()))


def processWarnings (str):
    """
    every warning come in all capital letters so to go into the format the function detects which
    warning it is and changes it to the correct format.

    """
    str = str.replace("_DEGREE_DETAIL", "")
    if str == "DEADSTORE":
        str = "Dead store"
    elif str == "UNINITIALIZEDMEMORY":
        str = "Uninitialized memory"
    elif str == "CASETERMINATION":
        str = "Case termination"
    elif str == "CHECKSTDLIBFUNCRETURN":
        str = "Check stdlibfunc return"
    elif str == "CFGINNONVOIDFUNC":
        str = " Cfg innnvoid function"
    elif str == "XFREE":
        str = "Xfree"
    elif str == "DOUBLEFREE":
        str = "Double free"
    return str


def main ():
    """

    The main function is to parse all the files that have been given as system argument


    """
    dicts = []
    d = jsonObject()
    ks = _keys
    # for k in range(2, len(sys.argv)):
    with open("parse.txt") as f:
        arr = f.readlines()
        n = 0
        while n < len(arr):
            line = arr[n]
            if "CFGINNONVOIDFUNC_DEGREE_DETAIL" in line:
                while "@" not in arr[n]:
                    n += 1
                line += arr[n]
                line = line.replace(";", "")
            elif "_DEGREE_DETAIL" not in line:
                n += 1
                continue
            line = line[:-1]
            line = line.replace("[", "")
            line = line.replace("]", " ")
            line = line.replace("(", "", 1)
            line = line.replace(")", " ", 1)
            line = line.replace(" @", "")
            line = line.replace("file ", "")
            line = line.lstrip()
            line = re.sub('/[^>]+/', '', line)
            line = re.sub('case.*?:', '', line)
            line = line.replace(':', ' ', 1)
            line = line.replace(' \t', " ")
            line = line.replace('\t', " ")
            line = line.replace('\n', '')
            val = line.split(" ", 5)
            del val[1]
            i = 0
            while i < len(_keys):
                if i == 0:
                    d[ks[i]] = processWarnings(val[i])
                elif i == 1:
                    d[ks[i]] = val[i]
                elif i == 2:
                    str = val[i].split(':')
                    d[ks[i]] = str[0]
                elif i == 3:
                    d[ks[i]] = processfeatures(val[i])
                i += 1
            if bool(d):
                dicts.append(d)
            d = jsonObject()
            n += 1


print("does this print twice?")
# print(dicts)
# print(json.dumps(dicts))


if __name__ == '__main__':
    main()
