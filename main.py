import json
from graduate import Graduate

with open("DB.json") as f:
    data = json.load(f)

graduates_dict = data["Graduates"]

# Search Functions

def __getIDsByFName(dict, fname):
    # type: (dict, str) -> list
    result_DB_IDs = list()
    for graduate in dict:
        if fname.lower() in graduate["First_Name"].lower():
            result_DB_IDs.append(graduate["DB_ID"])
    return result_DB_IDs


def __getIDsByLName(dict, lname):
    # type: (dict, str) -> list
    result_DB_IDs = list()
    for graduate in dict:
        if lname.lower() in graduate["Last_Name"].lower():
            result_DB_IDs.append(graduate["DB_ID"])
    return result_DB_IDs


def __getIDsByKey(dict, key):
    # type: (dict, str) -> list
    result_DB_IDs = __getIDsByFName(dict, key)
    result_DB_IDs.extend(id for id in __getIDsByLName(dict, key) if id not in result_DB_IDs)
    return result_DB_IDs


def __isLastEntry(graduates_list, graduateEntry):
    for graduate in graduates_list:
        if graduate.Last_DB_ID == graduateEntry.DB_ID:
            return False
    return True


def __filterDuplicateEntries(graduates_list):
    result_graduates = list()
    for graduate in graduates_list:
        if __isLastEntry(graduates_list, graduate):
            result_graduates.append(graduate)
    return result_graduates


def search(dict, key):
    # type: (dict, str) -> list
    result_graduates = list()
    result_DB_IDs = __getIDsByKey(dict, key)
    for graduate in dict:
        if graduate["DB_ID"] in result_DB_IDs:
            result_graduates.append(Graduate(graduate))
    return __filterDuplicateEntries(result_graduates)


graduates_list = search(graduates_dict, "a")
for result in graduates_list:
    print result