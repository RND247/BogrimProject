import json

with open("DB.json") as f:
    data = json.load(f)

Bogrim_dict = data["Bogrim"]

# Search Functions

def _getIDsByFName(dict, fname):
    # type: (dict, str) -> list
    result_DB_IDs = []
    for boger in dict:
        if fname in boger["First_Name"]:
            result_DB_IDs.append(boger["DB_ID"])
    return result_DB_IDs


def _getIDsByLName(dict, lname):
    # type: (dict, str) -> list
    result_DB_IDs = []
    for boger in dict:
        if lname in boger["Last_Name"]:
            result_DB_IDs.append(boger["DB_ID"])
    return result_DB_IDs


def _getIDsByKey(dict, key):
    # type: (dict, str) -> list
    result_DB_IDs = _getIDsByFName(dict, key)
    result_DB_IDs.extend(id for id in _getIDsByLName(dict, key) if id not in result_DB_IDs)
    return result_DB_IDs

def search(dict, key):
    result_bogrim = list()
    result_DB_IDs = _getIDsByKey(dict, key)
    for boger in dict:
        if boger["DB_ID"] in result_DB_IDs:
            result_bogrim.append(boger)
    return result_bogrim


for result in search(Bogrim_dict, "Al"):
    print result
    ## try and change
