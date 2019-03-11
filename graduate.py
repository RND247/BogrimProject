from datetime import date

class Graduate:

    def __init__(self, graduate_info_list):
        self.DB_ID = graduate_info_list["DB_ID"]
        self.Last_DB_ID = graduate_info_list["Last_DB_ID"]
        self.ID_number = graduate_info_list["ID_number"]
        self.First_Name = graduate_info_list["First_Name"]
        self.Last_Name = graduate_info_list["Last_Name"]
        self.Date_Of_Birth = graduate_info_list["Date_Of_Birth"]
        self.Current_Work_Place = graduate_info_list["Current_Work_Place"]
        self.Job_Title = graduate_info_list["Job_Title"]
        self.Work_Field = graduate_info_list["Work_Field"]
        self.Notes = graduate_info_list["Notes"]

    def __str__(self):
        return self.First_Name + " " + self.Last_Name + " " + str(self.calculateAge())

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