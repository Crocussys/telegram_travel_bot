from os import getenv
from pathlib import Path

class Environments(dict):
    def __init__(self):
        super().__init__()

        self.update({
            "work_dir":      getenv("WORK_DIR"),
            "customer_file": getenv("CUSTOMER_FILE")
        })
        self.update({"conf_dir": f"{self["work_dir"]}/conf"})

        secrets_files = getenv("SECTRETS_ENV_FILES").split(";")
        for secret_file_path in secrets_files:
            self.update({data[:data.find("=")]: data[data.find("=") + 1:] for data in Path(secret_file_path).read_text().split("\n")})
