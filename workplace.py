class Workplace:

    def __init__(self, workplace_info_dict):
        self.name = workplace_info_dict["Name"]
        self.location = workplace_info_dict["Location"]
        self.image = workplace_info_dict["Image"]

    def __str__(self):
        return self.name

    def to_dict(self):
        """
        Takes all the workplace's attributes and returns it in a form of dict.
        :return: a dict.
        """
        workplace_dict = dict()
        workplace_dict["Name"] = self.name
        workplace_dict["Location"] = self.location
        workplace_dict["Image"] = self.image
        return workplace_dict
