from annual_report.report_data.report_data import find_elements_based_pattern, make_combinations


class TestReportData():
    """Tests for report data class."""

    def test_find_elements_based_pattern(self):
        """Find main account codes based on pattern"""
        classification = "MAJANDUSLIKSISU2024ap"
        pattern = "^101\\d{3}$"

        element_list = find_elements_based_pattern(classification, pattern)
        assert len(element_list) == 4

    def test_make_combinations_first_list_1_element_second_3_elements(self):
        list1 = ["ACCOUNT1"]
        list2 = ["VG_201", "VG_202", "VG_203"]
        combinations = make_combinations(list1, list2)
        assert len(combinations) == 3
        assert combinations[1] == "ACCOUNT1-VG_202"

    def test_make_combinations_first_list_2_element_second_3_elements(self):
        list1 = ["ACCOUNT1", "ACCOUNT2"]
        list2 = ["VG_201", "VG_202", "VG_203"]
        combinations = make_combinations(list1, list2)
        assert len(combinations) == 6

    def test_make_combinations_first_list_2_element_second_1_elements(self):
        list1 = ["ACCOUNT1", "ACCOUNT2"]
        list2 = ["*"]

        combinations = make_combinations(list1, list2)
        assert len(combinations) == 2
        assert combinations[1] == "ACCOUNT2-*"
