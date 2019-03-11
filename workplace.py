class Workplace:

    def __init__(self, workplace_info_dict):
        self.name = workplace_info_dict["Name"]
        self.location = workplace_info_dict["Location"]

    def __str__(self):
        return self.name
