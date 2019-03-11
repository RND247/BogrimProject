import json
from graduate import Graduate

with open("DB.json") as f:
    data = json.load(f)


# Checks if the given entry is the last (most recent) entry for the graduate in the DB.
def __isLastEntry(graduates_dict, graduateEntry):
    # types: (dict, Graduate) -> bool
    for id, graduate in graduates_dict.iteritems():
        if graduate.Last_DB_ID == graduateEntry.DB_ID:
            return False
    return True


# Takes a dictionary of graduates and filter it so every graduate will appear only once with its last entry.
def __filterDuplicateEntriesDict(graduates_dict):
    # types: (dict) -> dict
    result_graduates_dict = dict()
    for id, graduate in graduates_dict.iteritems():
        if __isLastEntry(graduates_dict, graduate):
            result_graduates_dict[id] = graduate
    return result_graduates_dict


DB_graduates_dict = data["Graduates"]
full_graduates_dict = dict()  # Graduates Dictionary with all the graduates' entries from the DB.
for val in DB_graduates_dict:
    full_graduates_dict[val["DB_ID"]] = Graduate(val)
no_dup_graduates_dict = __filterDuplicateEntriesDict(full_graduates_dict)  # Graduates Dictionary with only the last
                                                                            # entry for each graduate.


def __getIDsByKey(dict, key):
    # type: (dict, str) -> list
    result_DB_IDs = list()
    for id, graduate in dict.iteritems():
        if key.lower() in str(graduate).lower():
            result_DB_IDs.append(id)
    return result_DB_IDs


def search(graduates_dict, key):
    # type: (dict, str) -> list
    result_graduates = list()
    result_DB_IDs = __getIDsByKey(graduates_dict, key)
    for id, graduate in graduates_dict.iteritems():
        if graduate.DB_ID in result_DB_IDs:
            result_graduates.append(graduate)
    return result_graduates


def getEveryEntry(graduate):
    allEntriesList = list()
    while graduate.Last_DB_ID is not None:
        allEntriesList.append(graduate)
        graduate = full_graduates_dict[graduate.Last_DB_ID]
    allEntriesList.append(graduate)
    return allEntriesList

# test runs /*
graduates_list = search(no_dup_graduates_dict, "n")
for result in graduates_list:
    print str(result)
print "\n"
gr = full_graduates_dict[3]
for entry in getEveryEntry(gr):
    print entry.Job_Title + " at " + entry.Current_Work_Place

# */