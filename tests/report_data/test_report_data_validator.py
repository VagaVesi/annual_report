from json import loads
from path import Path
from report_data.report_data_validator import ReportDataValidator


class TestReportDataValidator():
    """Tests for report data validator."""

    def test_find_total_amount_1_element(self):
        """Return total amount one element"""
        element_codes = ["BS-AssetsShort-Cash"]
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_ok.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        amount = report_data.find_total_amount(element_codes)

        assert amount == 4100.0

    def test_find_total_amount_2_elements(self):
        """Return total amount of debit and credit balance elements"""
        element_codes = ["IS-Revenue", "IS1-Expenses-OtherOperatingExpenses"]
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_ok.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        amount = report_data.find_total_amount(element_codes)

        assert amount == 1250.0

    def test_find_target_element_return_1_validation_rule(self):
        """Select validation rules based on report elements"""

        element_code = "BS-LiabilitiesAndEquity-Total"
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_ok.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        validation_rules = report_data.add_target_element_validation_rules(
            element_code)

        assert validation_rules[0]["id"] == 1

    def test_find_target_element_return_2_validation_rules(self):
        """Select validation rules based on report elements"""

        element_code = "Note-Cash-Total"
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_ok.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        validation_rules = report_data.add_target_element_validation_rules(
            element_code)

        assert validation_rules[0]["id"] == 2
        assert validation_rules[1]["id"] == 5

    def test_validate_report_data_ok(self):
        """Validate report data with no errors."""
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_ok.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        errors = report_data.validate()

        assert len(errors) == 0

    def test_validate_report_data_with_errors(self):
        """Validate report data with errors."""
        path = Path(
            "annual_report/tests/report_data/source_data/test_data_for_xbrl_errors.json")
        if path.exists():
            report_data = ReportDataValidator(
                loads(path.read_text(encoding="utf-8")))

        errors = report_data.validate()

        assert len(errors) > 0
