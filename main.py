import json
from graduate import Graduate
from workplace import Workplace

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
DB_workplaces_dict = data["Workplaces"]
full_graduates_dict = dict()  # Graduates Dictionary with all the graduates' entries from the DB.
for val in DB_graduates_dict:
    full_graduates_dict[val["DB_ID"]] = Graduate(val)
no_dup_graduates_dict = __filterDuplicateEntriesDict(full_graduates_dict)  # Graduates Dictionary with only the last
                                                                            # entry for each graduate.
full_workplaces_dict = dict()  # Workplaces Dictionary with all the workplaces' entries from the DB.
for val in DB_workplaces_dict:
    full_workplaces_dict[val["Name"]] = Workplace(val)


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
    all_entries_list = list()
    while graduate.Last_DB_ID is not None:
        all_entries_list.append(graduate)
        graduate = full_graduates_dict[graduate.Last_DB_ID]
    all_entries_list.append(graduate)
    return all_entries_list


# test runs /*
graduates_list = search(no_dup_graduates_dict, "al")
for result in graduates_list:
    print str(result)
print "\n"
gr = no_dup_graduates_dict[3]
for entry in getEveryEntry(gr):
    print entry.Job_Title + " at " + entry.Current_Work_Place

# */
