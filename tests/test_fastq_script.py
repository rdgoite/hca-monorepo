import json
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from common.validation_report import ValidationReport
from script.fastq import Fastq


class TestFastqScript(TestCase):

    def test_prints_out_valid_report(self):
        # given:
        report = ValidationReport.validation_report_ok()

        # when:
        json_output = self._do_execute_print_report(report)

        # then:
        self.assertEqual("VALID", json_output["validation_state"])

    def test_prints_out_invalid_report(self):
        # given:
        report = ValidationReport("INVALID")
        report.log_error("Invalid sequence characters.")

        json_output = self._do_execute_print_report(report)

        # then:
        self.assertEqual("INVALID", json_output["validation_state"])

    def _do_execute_print_report(self, expected_report):
        with patch('validator.fastq.Validator') as validator:
            # given:
            validator.validate.return_value = expected_report

            # and:
            fastq = Fastq(validator)

            # when:
            path_to_file = "path/to/file.fastq"
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                fastq.executeOn(path_to_file)

            # then:
            validator.validate.assert_called_once_with(path_to_file)

            # and:
            stdout_value = mock_stdout.getvalue().strip()
            assert stdout_value
            return json.loads(stdout_value)