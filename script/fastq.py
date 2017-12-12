class Fastq:

    def __init__(self, validator):
        self.validator = validator

    def executeOn(self, file_path):
        self.validator.validate(file_path)
        print('{"validation_state" : "VALID"}')