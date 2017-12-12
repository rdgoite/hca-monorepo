import json


class Fastq:

    def __init__(self, validator):
        self.validator = validator

    def executeOn(self, file_path):
        report = self.validator.validate(file_path)
        report_map = {'validation_state': report.validation_state}
        print(json.dumps(report_map))