import json
from graduate import Graduate

with open("DB.json") as f:
    data = json.load(f)

graduates_dict = data["Graduates"]

# Search Functions

def _getIDsByFName(dict, fname):
    # type: (dict, str) -> list
    result_DB_IDs = []
    for graduate in dict:
        if fname in graduate["First_Name"]:
            result_DB_IDs.append(graduate["DB_ID"])
    return result_DB_IDs


def _getIDsByLName(dict, lname):
    # type: (dict, str) -> list
    result_DB_IDs = []
    for graduate in dict:
        if lname in graduate["Last_Name"]:
            result_DB_IDs.append(graduate["DB_ID"])
    return result_DB_IDs


def _getIDsByKey(dict, key):
    # type: (dict, str) -> list
    result_DB_IDs = _getIDsByFName(dict, key)
    result_DB_IDs.extend(id for id in _getIDsByLName(dict, key) if id not in result_DB_IDs)
    return result_DB_IDs

def search(dict, key):
    result_graduates = list()
    result_DB_IDs = _getIDsByKey(dict, key)
    for graduate in dict:
        if graduate["DB_ID"] in result_DB_IDs:
            result_graduates.append(graduate)
    return result_graduates


graduates_list = list()
for result in search(graduates_dict, "a"):
    graduates_list.append(Graduate(result))
    print Graduate(result)
