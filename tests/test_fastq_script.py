from unittest import TestCase
from unittest.mock import patch

from io import StringIO

import json

from common.validationreport import ValidationReport
from script.fastq import Fastq


class TestFastqScript(TestCase):

    def test_prints_out_valid_report(self):
        with patch('validator.fastq.Validator') as validator:
            # given:
            validator.validate.return_value = ValidationReport.validation_report_ok()

            # and:
            fastq = Fastq(validator)

            # when:
            path_to_file = 'path/to/file.fastq'
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                fastq.executeOn(path_to_file)

            # then:
            validator.validate.assert_called_once_with(path_to_file)

            # and:
            stdout_value = mock_stdout.getvalue().strip()
            json_output = json.loads(stdout_value)
            self.assertEqual("VALID", json_output["validation_state"])

    def test_prints_out_invalid_report(self):
        with patch('validator.fastq.Validator') as validator:
            # given:
            validator.validate.return_value = ValidationReport("INVALID")

            # and:
            fastq = Fastq(validator)

            # when:
            path_to_file = "path/to/file.fastq"
            fastq.executeOn(path_to_file)

            # then:
            validator.validate.assert_called_once_with(path_to_file)