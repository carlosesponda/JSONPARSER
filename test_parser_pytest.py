import json
import subprocess
import pytest
from parser import *

def test_output():
    with open('uclibc.txt') as json_file:
        try:
            json_object = json.load(json_file)
        except ValueError as e:
            pytest.fail("json validation failed")
        pass

def test_main():
    result = subprocess.check_call(["find","-name" , "*vaa_detailreport", "|", "parallel", "--xargs", "python", "../parser.py", "test"])

    if result == 0:
        pass
    else:
        pytest.fail()

def test_processfeature():
    result = processfeatures("!defSQLITE_ENABLE_COLUMN_METADATA|!defSQLITE_OMIT_DECLTYPE")
    if result == ["-SQLITE_ENABLE_COLUMN_METADATA", "-SQLITE_OMIT_DECLTYPE"]:
        pass
    else:
        pytest.fail()

def test_processfilename():
    result = processWarnings("DOUBLEFREE")
    if result == "Double free":
        pass
    else:
        pytest.fail()
