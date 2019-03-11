from datetime import date


class Graduate:

    def __init__(self, graduate_info_dict):
        self.DB_ID = graduate_info_dict["DB_ID"]
        self.Last_DB_ID = graduate_info_dict["Last_DB_ID"]
        self.ID_Number = graduate_info_dict["ID_Number"]
        self.First_Name = graduate_info_dict["First_Name"]
        self.Last_Name = graduate_info_dict["Last_Name"]
        self.Date_Of_Birth = graduate_info_dict["Date_Of_Birth"]
        self.Current_Work_Place = graduate_info_dict["Current_Work_Place"]
        self.Job_Title = graduate_info_dict["Job_Title"]
        self.Work_Field = graduate_info_dict["Work_Field"]
        self.Notes = graduate_info_dict["Notes"]

    def __str__(self):
        return self.First_Name + " " + self.Last_Name + " " + str(self.calculateAge())

    def toDict(self):
        graduate_dict = dict()
        graduate_dict["DB_ID"] = self.DB_ID
        graduate_dict["Last_DB_ID"] = self.Last_DB_ID
        graduate_dict["ID_Number"] = self.ID_Number
        graduate_dict["First_Name"] = self.First_Name
        graduate_dict["Last_Name"] = self.Last_Name
        graduate_dict["Date_Of_Birth"] = self.Date_Of_Birth
        graduate_dict["Current_Work_Place"] = self.Current_Work_Place
        graduate_dict["Job_Title"] = self.Job_Title
        graduate_dict["Work_Field"] = self.Work_Field
        graduate_dict["Notes"] = self.Notes
        return graduate_dict

    def __dateOfBirthToDateTime(self):
        dateOfBirth_int = list()
        dateOfBirth_str = self.Date_Of_Birth.split("/")
        for val in dateOfBirth_str:
            dateOfBirth_int.append(int(val))
        return date(dateOfBirth_int[2], dateOfBirth_int[1],dateOfBirth_int[0])

    def calculateAge(self):
        today = date.today()
        dateOfBirth = self.__dateOfBirthToDateTime()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        return age
