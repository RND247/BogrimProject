from datetime import date


class Graduate:

    def __init__(self, graduate_info_dict):
        self.time_stamp = graduate_info_dict["Time_Stamp"]
        self.db_id = graduate_info_dict["DB_ID"]
        self.last_db_id = graduate_info_dict["Last_DB_ID"]
        self.id_number = graduate_info_dict["ID_Number"]
        self.first_name = graduate_info_dict["First_Name"]
        self.last_name = graduate_info_dict["Last_Name"]
        self.date_of_birth = graduate_info_dict["Date_Of_Birth"]
        self.current_work_place = graduate_info_dict["Current_Work_Place"]
        self.job_title = graduate_info_dict["Job_Title"]
        self.work_field = graduate_info_dict["Work_Field"]
        self.notes = graduate_info_dict["Notes"]

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.calculate_age())

    def to_dict(self):
        """
        Takes all the graduate's attributes and return it in a form of dict.
        :return: a dict.
        """
        graduate_dict = dict()
        graduate_dict["Time_Stamp"] = self.time_stamp
        graduate_dict["DB_ID"] = self.db_id
        graduate_dict["Last_DB_ID"] = self.last_db_id
        graduate_dict["ID_Number"] = self.id_number
        graduate_dict["First_Name"] = self.first_name
        graduate_dict["Last_Name"] = self.last_name
        graduate_dict["Date_Of_Birth"] = self.date_of_birth
        graduate_dict["Current_Work_Place"] = self.current_work_place
        graduate_dict["Job_Title"] = self.job_title
        graduate_dict["Work_Field"] = self.work_field
        graduate_dict["Notes"] = self.notes
        return graduate_dict

    def __date_of_birth_to_datetime(self):
        """
        Takes the Date_Of_Birth attribute and transfers and returns it in a form of datetime.
        :return: a datetime.
        """
        date_of_birth_int = list()
        date_of_birth_str = self.date_of_birth.split("/")
        for val in date_of_birth_str:
            date_of_birth_int.append(int(val))
        return date(date_of_birth_int[2], date_of_birth_int[1],date_of_birth_int[0])

    def calculate_age(self):
        """
        Calculates and returns the age of the graduate.
        :return: an integer, representing the calculated age.
        """
        today = date.today()
        date_of_birth = self.__date_of_birth_to_datetime()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
