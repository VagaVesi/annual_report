from annual_report.report_data.report_data import find_elements_based_pattern


class TestReportData():
    """Tests for report data class."""

    def test_find_elements_based_pattern(self):
        """Find main account codes based on pattern"""
        classification = "MAJANDUSLIKSISU2024ap"
        pattern = "^101\\d{3}$"

        element_list = find_elements_based_pattern(classification, pattern)
        assert len(element_list) == 4
