import json
import time
import datetime
from graduate import Graduate
from workplace import Workplace

with open("DB.json") as f:
    data = json.load(f)


# Gets a graduate and checks if the given entry is the last (most recent) entry for the graduate in the DB.
def __isLastEntry(graduateEntry):
    # types: (Graduate) -> bool
    for id, graduate in full_graduates_dict.iteritems():
        if graduate.last_db_id == graduateEntry.db_id:
            return False
    return True


# Takes the full_graduate_dict and builds a new dict so every graduate will appear only once with its last entry.
def __filterDuplicateEntriesDict():
    # types: () -> dict
    result_graduates_dict = dict()
    for id, graduate in full_graduates_dict.iteritems():
        if __isLastEntry(graduate):
            result_graduates_dict[id] = graduate
    return result_graduates_dict


DB_graduates_dict = data["Graduates"] # Gets the graduates list from the json file.
DB_workplaces_dict = data["Workplaces"] # Gets the workplaces list from the json file.
full_graduates_dict = dict()  # Graduates dictionary with all the graduates' entries from the DB.
for val in DB_graduates_dict:
    full_graduates_dict[val["DB_ID"]] = Graduate(val)
no_dup_graduates_dict = __filterDuplicateEntriesDict()  # Graduates Dictionary with only the last
                                                        #   entry for each graduate.
full_workplaces_dict = dict()  # Workplaces dictionary with all the workplaces' entries from the DB.
for val in DB_workplaces_dict:
    full_workplaces_dict[val["Name"]] = Workplace(val)


# Gets a dict and a key and returns a list of all the dict's keys that their values' strings include the key.
def __getIDsByKey(dict, key):
    # type: (dict, str) -> list
    result_DB_IDs = list()
    for id, graduate in dict.iteritems():
        if key.lower() in str(graduate).lower():
            result_DB_IDs.append(id)
    return result_DB_IDs


# Gets a key and returns a list of all the values in no_dup_graduate_dict that their IDs returned in the __getIDsByKey
#   function with the given key.
def searchGraduateByName(key):
    # type: (str) -> list
    result_graduates = list()
    result_DB_IDs = __getIDsByKey(no_dup_graduates_dict, key)
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.db_id in result_DB_IDs:
            result_graduates.append(graduate)
    return result_graduates


# Gets a workplace and returns a list of all the values in full_graduates_dict that their Work_Place attribute equals to
#   the given workplace
def searchGraduateByWorkPlace(workplace):
    # type: (str) -> list
    result_graduates = list()
    for id, graduate in full_graduates_dict.iteritems():
        if graduate.current_work_place.lower() == workplace.lower():
            result_graduates.append(graduate)
    return result_graduates


# Gets an id_number and returns a value from no_dup_graduates_dict if its id_number attribute is equal to the given
#   id_number, else it returns None.
def __searchGraduateByIDNumber(ID_Number):
    # type: (str) -> Graduate
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.id_number == ID_Number:
            return graduate
    return None


# Gets a graduate and returns a list of all the values from full_graduates_dict that belong to the given graduate
def getEveryEntry(graduate):
    # type: (Graduate) -> list
    all_entries_list = list()
    while graduate.last_db_id is not None:
        all_entries_list.append(graduate)
        graduate = full_graduates_dict[graduate.last_db_id]
    all_entries_list.append(graduate)
    return all_entries_list


# Builds and returns a dictionary of Graduates and Workplaces based on the full_graduates_dict and the
#   full_workplaces_dict dicts.
def __buildJsonDict():
    # type: () -> dict
    newJsonDict = dict()
    graduates_dicts_list = list()
    workplaces_dicts_list = list()
    for id, graduate in full_graduates_dict.iteritems():
        graduates_dicts_list.append(graduate.toDict())
    for id, workplace in full_workplaces_dict.iteritems():
        workplaces_dicts_list.append(workplace.toDict())
    newJsonDict["Graduates"] = graduates_dicts_list
    newJsonDict["Workplaces"] = workplaces_dicts_list
    return newJsonDict


# Gets a string in a form of a dict and dumps it as a json content into a given file path. Returns True.
def __writeToJsonFile(dict, jsonFilePath="DB.json"):
    # type: (dict, str) -> bool
    with open(jsonFilePath, "w") as f:
        json.dump(dict, f, indent=2)
    return True


# Using the private methods __buildJsonDict and __writeToJsonFile to update the json file with the current dicts
#   entries. Returns True.
def __updateJsonFile():
    # type: () -> bool
    __writeToJsonFile(__buildJsonDict())
    return True


# Walks through the full_graduates_dict's keys and returns the biggest ID in the list + 1.
def __getNextID():
    # type: () -> int
    lastID = 0
    for ID in full_graduates_dict:
        if ID > lastID:
            lastID = ID
    return lastID+1


# Adds a new Graduate to the full_graduates_dict and then builds the DB.json.
# The function aims for new graduates only as it checks if the id_number already exist in the full_graduates_dict.
def addNewGraduate((id_number, first_name, last_name, date_of_birth, current_work_place, job_title, work_field, notes)):
    # type: (list) -> bool
    if __searchGraduateByIDNumber(id_number) is None:
        graduate_info_dict = dict()
        next_id = __getNextID()
        time_stamp_sec = time.time()
        time_stamp = datetime.datetime.fromtimestamp(time_stamp_sec).strftime("%Y-%m-%d %H:%M:%S")
        graduate_info_dict["Time_Stamp"] = time_stamp
        graduate_info_dict["DB_ID"] = next_id
        graduate_info_dict["Last_DB_ID"] = None
        graduate_info_dict["ID_Number"] = id_number
        graduate_info_dict["First_Name"] = first_name
        graduate_info_dict["Last_Name"] = last_name
        graduate_info_dict["Date_Of_Birth"] = date_of_birth
        graduate_info_dict["Current_Work_Place"] = current_work_place
        graduate_info_dict["Job_Title"] = job_title
        graduate_info_dict["Work_Field"] = work_field
        graduate_info_dict["Notes"] = notes
        full_graduates_dict[next_id] = Graduate(graduate_info_dict)
        __updateJsonFile()
        return True
    return False


# test runs /*
graduates_list = searchGraduateByWorkPlace("Matzov")
for result in graduates_list:
    print str(result) + " " + str(__isLastEntry(result))
print "\n"
gr = no_dup_graduates_dict[9]
for entry in getEveryEntry(gr):
    print entry.job_title + " at " + entry.current_work_place
addNewGraduate(("205786122","TRan","Dayan","24/7/1994","Google","CEO", "Management", ""))
# */
