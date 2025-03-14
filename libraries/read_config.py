import json

class ReadConfig:
    """
    Class representing the read configuration from json file.
    """
    def __init__(self, config_file):
        self.config_file = config_file

    def read_config(self):
        with open(self.config_file) as json_file:
            config = json.load(json_file)
            return config