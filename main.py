import json
import time
import datetime
from graduate import Graduate
from workplace import Workplace

with open("DB.json") as f:
    data = json.load(f)


def __is_last_entry(graduateEntry):
    """
    Gets a graduate and checks if the given entry is the last (most recent) entry for the graduate in the DB.
    :param graduateEntry: Graduate type, a graduate to check in the full_graduates_dict if it is the last entry for it.
    :return: True if it's the last entry for the given graduateEntry, False otherwise.
    """
    for id, graduate in full_graduates_dict.iteritems():
        if graduate.last_db_id == graduateEntry.db_id:
            return False
    return True


def __filter_duplicate_entries_dict():
    """
    Takes the full_graduate_dict and builds a new dict so every graduate will appear only once with its last entry.
    :return: a dict type, contains only the last entry for each graduate in the full_graduate_dict.
    """
    result_graduates_dict = dict()
    for id, graduate in full_graduates_dict.iteritems():
        if __is_last_entry(graduate):
            result_graduates_dict[id] = graduate
    return result_graduates_dict


db_graduates_dict = data["Graduates"] # Gets the graduates list from the json file.
db_workplaces_dict = data["Workplaces"] # Gets the workplaces list from the json file.
full_graduates_dict = dict()  # Graduates dictionary with all the graduates' entries from the DB.
for val in db_graduates_dict:
    full_graduates_dict[val["DB_ID"]] = Graduate(val)
no_dup_graduates_dict = __filter_duplicate_entries_dict()  # Graduates Dictionary with only the last
                                                        #   entry for each graduate.
full_workplaces_dict = dict()  # Workplaces dictionary with all the workplaces' entries from the DB.
for val in db_workplaces_dict:
    full_workplaces_dict[val["Name"]] = Workplace(val)


def __get_ids_by_key(dict, key):
    """
    Gets a dict and a key and returns a list of all the dict's keys that their values' strings include the key.
    :param dict: a dict to run on its' values while looking for the key.
    :param key: a string, a word to look for in the dicts' values.
    :return: a list of dicts' keys for the dicts' values that matched the key search.
    """
    result_db_ids = list()
    for id, graduate in dict.iteritems():
        if key.lower() in str(graduate).lower():
            result_db_ids.append(id)
    return result_db_ids


def search_graduate_by_name(key):
    """
    Gets a key and returns a list of all the values in no_dup_graduate_dict that their ids returned in the __get_ids_by_key
    function with the given key.
    :param key: a string. a word to look for in the no_dup_graduates_dict.
    :return: a list of Graduates.
    """
    result_graduates = list()
    result_db_ids = __get_ids_by_key(no_dup_graduates_dict, key)
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.db_id in result_db_ids:
            result_graduates.append(graduate)
    return result_graduates


def search_graduate_by_workplace(workplace):
    """
    Gets a workplace and returns a list of all the values in full_graduates_dict that their work_place attribute equals
    to the given workplace
    :param workplace: a string, representing a workplace to look for in the values of the full_graduates_dict.
    :return: a list of Graduates.
    """
    result_graduates = list()
    for id, graduate in full_graduates_dict.iteritems():
        if graduate.current_work_place.lower() == workplace.lower():
            result_graduates.append(graduate)
    return result_graduates


def __search_graduate_by_id_number(id_number):
    """
    Gets an id_number and returns a value from no_dup_graduates_dict if its id_number attribute is equal to the given
    id_number, else it returns None.
    :param id_number: a string, an id number to look for in the values of no_dup_graduates_dict.
    :return: a Graduate with matching value in its id_number attribute, None if no one found.
    """
    for id, graduate in no_dup_graduates_dict.iteritems():
        if graduate.id_number == id_number:
            return graduate
    return None


def get_every_entry(graduate):
    """
    Gets a graduate and returns a list of all the values from full_graduates_dict that belong to the given graduate.
    :param graduate: a Graduate, for whom it looks for other entries in the full_graduates_dict.
    :return: a list of Graduates.
    """
    all_entries_list = list()
    while graduate.last_db_id is not None:
        all_entries_list.append(graduate)
        graduate = full_graduates_dict[graduate.last_db_id]
    all_entries_list.append(graduate)
    return all_entries_list


def __build_json_dict():
    """
    Builds and returns a dictionary of Graduates and Workplaces based on the full_graduates_dict and the
    full_workplaces_dict dicts.
    :return: a dict with keys of "Graduates" and "Workplaces".
    """
    new_json_dict = dict()
    graduates_dicts_list = list()
    workplaces_dicts_list = list()
    for id, graduate in full_graduates_dict.iteritems():
        graduates_dicts_list.append(graduate.to_dict())
    for id, workplace in full_workplaces_dict.iteritems():
        workplaces_dicts_list.append(workplace.to_dict())
    new_json_dict["Graduates"] = graduates_dicts_list
    new_json_dict["Workplaces"] = workplaces_dicts_list
    return new_json_dict


def __write_to_json_file(dict, json_file_path="DB.json"):
    """
    Gets a dict and dumps it as a json content into a given file path. Returns True.
    :param dict: dict to write into the json file.
    :param json_file_path: path for a json file. default: "DB.json".
    :return: True.
    """
    with open(json_file_path, "w") as f:
        json.dump(dict, f, indent=2)
    return True


def __update_json_file():
    """
    Using the private methods __build_json_dict and __write_to_json_file to update the json file with the current dicts
#   entries.
    :return: True.
    """
    __write_to_json_file(__build_json_dict())
    return True


def __get_next_id():
    """
    Walks through the full_graduates_dict's keys and returns the biggest id in the list + 1.
    :return: an integer, with a value of the biggest id in the full_graduates_dict + 1.
    """
    last_id = 0
    for id in full_graduates_dict:
        if id > last_id:
            last_id = id
    return last_id+1


def add_new_graduate((id_number, first_name, last_name, date_of_birth, current_work_place, job_title, work_field,
                     notes)):
    """
    Adds a new Graduate to the full_graduates_dict and then builds the DB.json.
    The function aims for new graduates only as it checks if the id_number already exist in the full_graduates_dict.
    :return: True if the graduate has been added, False otherwise.
    """
    if __search_graduate_by_id_number(id_number) is None:
        graduate_info_dict = dict()
        next_id = __get_next_id()
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
        __update_json_file()
        return True
    return False


# test runs /*
graduates_list = search_graduate_by_workplace("Matzov")
for result in graduates_list:
    print str(result) + " " + str(__is_last_entry(result))
print "\n"
gr = no_dup_graduates_dict[9]
for entry in get_every_entry(gr):
    print entry.job_title + " at " + entry.current_work_place
add_new_graduate(("205786122", "TRan", "Dayan", "24/7/1994", "Google", "CEO", "Management", ""))
# */
