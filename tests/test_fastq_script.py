import json
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from common.validationreport import ValidationReport
from script.fastq import Fastq


class TestFastqScript(TestCase):

    def test_prints_out_valid_report(self):
        # expect:
        report = ValidationReport.validation_report_ok()
        json_assert = lambda json_output: \
            self.assertEqual("VALID", json_output["validation_state"])
        self._do_test_prints_report(report, json_assert)

    def test_prints_out_invalid_report(self):
        # expect:
        report = ValidationReport("INVALID")
        json_assert = lambda json_output: \
            self.assertEqual("INVALID", json_output["validation_state"])
        self._do_test_prints_report(report, json_assert)


    def _do_test_prints_report(self, expected_report, json_assert):
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
            json_assert(json.loads(stdout_value))
