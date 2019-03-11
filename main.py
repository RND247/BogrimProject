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


def searchGraduateByName(key):
    # type: (str) -> list
    result_graduates = list()
    result_DB_IDs = __getIDsByKey(no_dup_graduates_dict, key)
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.DB_ID in result_DB_IDs:
            result_graduates.append(graduate)
    return result_graduates


def __searchGraduateByIDNumber(ID_Number):
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.ID_Number == ID_Number:
            return graduate
    return None


def getEveryEntry(graduate):
    all_entries_list = list()
    while graduate.Last_DB_ID is not None:
        all_entries_list.append(graduate)
        graduate = full_graduates_dict[graduate.Last_DB_ID]
    all_entries_list.append(graduate)
    return all_entries_list


def __buildJsonDict():
    newJsonDict = dict()
    graduates_dicts_list = list()
    workplaces_dicts_list = list()
    for id, graduate in full_graduates_dict.iteritems():
        graduates_dicts_list.append(graduate.toDict())
    for id, workplace in full_workplaces_dict.iteritems():
        workplaces_dicts_list.append(workplace.toDict())
    newJsonDict["Graduates"] = graduates_dicts_list
    newJsonDict["Workplaces"] = workplaces_dicts_list
    with open("DB.json", "w") as f:
        json.dump(newJsonDict, f, indent=3)
        f.close()


def __getNextID():
    lastID = 0
    for ID in full_graduates_dict:
        if ID > lastID:
            lastID = ID
    return lastID+1


# Adds a new Graduate to the full_graduates_dict and then builds the DB.json.
# The function aims for new graduates only as it checks if the ID_Number already exist in the full_graduates_dict.
def addNewGraduate((ID_Number, First_Name, Last_Name, Date_Of_Birth, Current_Work_Place, Job_Title, Work_Field, Notes)):
    if __searchGraduateByIDNumber(ID_Number) is None:
        graduate_info_dict = dict()
        graduate_info_dict["DB_ID"] = __getNextID()
        graduate_info_dict["Last_DB_ID"] = None
        graduate_info_dict["ID_Number"] = ID_Number
        graduate_info_dict["First_Name"] = First_Name
        graduate_info_dict["Last_Name"] = Last_Name
        graduate_info_dict["Date_Of_Birth"] = Date_Of_Birth
        graduate_info_dict["Current_Work_Place"] = Current_Work_Place
        graduate_info_dict["Job_Title"] = Job_Title
        graduate_info_dict["Work_Field"] = Work_Field
        graduate_info_dict["Notes"] = Notes
        full_graduates_dict[__getNextID()] = Graduate(graduate_info_dict)
        __buildJsonDict()
    else:
        return False


# test runs /*
graduates_list = searchGraduateByName("al")
for result in graduates_list:
    print str(result)
print "\n"
gr = no_dup_graduates_dict[3]
for entry in getEveryEntry(gr):
    print entry.Job_Title + " at " + entry.Current_Work_Place
#addNewGraduate(("424242244","Alex","Shimoni","11/7/1991","IBM Israel","Junior Programmer", "OS", ""))
# */
