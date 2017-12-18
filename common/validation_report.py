class ValidationError:

    def __init__(self, user_friendly_message):
        self.user_friendly_message = user_friendly_message

class ValidationReport:

    def __init__(self, state="", error_reports=None):
        self.state = state
        self.errors = error_reports if error_reports is not None else list()  # list of ErrorReport

    def errors_to_dict(self):
        return [error.to_dict() for error in self.errors]

    def log_error(self, user_friendly_message):
        self.errors.append(ValidationError(user_friendly_message))

    def to_dict(self):
        return {
            "validation_state": self.state
        }

    @staticmethod
    def validation_report_ok():
        report = ValidationReport()
        report.state = "VALID"
        return report
