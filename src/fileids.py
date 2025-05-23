import json


class Files:
    def __init__(self, conf_file_path):
        with open(conf_file_path, "r") as conf_file:
            self.conf = json.loads(conf_file.read())
    
    def get(self):
        return self.conf
    
    def photo(self, name):
        return self.conf["photos"].get(name)
    
    def doc(self, name):
        return self.conf["documents"].get(name)
