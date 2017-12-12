import json


class Fastq:

    def __init__(self, validator):
        self.validator = validator

    def executeOn(self, file_path):
        report = self.validator.validate(file_path)
        json_value = json.dumps(report.__dict__)
        print(json_value)