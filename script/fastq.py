#!/usr/bin/env python

import json
import sys

from validator.fastq import Validator


class Fastq:

    def __init__(self, validator):
        self.validator = validator

    def executeOn(self, file_path):
        report = self.validator.validate(file_path)
        json_value = json.dumps(report.__dict__)
        print(json_value)


if __name__ == '__main__':
    validator = Validator()
    Fastq(validator).executeOn(sys.argv[1])