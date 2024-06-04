from json import loads
from path import Path
from annual_report.report_data.report_data import ReportData, ReportElement, find_gl_element_codes_based_pattern, make_combinations


class TestReportData():
    """Tests for report data class."""

    def test_find_elements_based_pattern(self):
        """Find main account codes based on pattern"""
        classification = "MAJANDUSLIKSISU2024ap"
        pattern = "^101\\d{3}$"

        element_list = find_gl_element_codes_based_pattern(
            classification, pattern)
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

    def test_report_data_is_element_in_list(self):
        """Test returning elements by name if they """
        path = Path(
            "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
        sample_dataset = loads(path.read_text(encoding="utf-8"))
        report_data = ReportData(sample_dataset)
        report_element = ReportElement("BS-AssetsShort-Cash")
        report_data.report_elements.append(report_element)

        assert report_data.is_element_in_list(
            "BS-AssetsShort-Cash") == [report_element]
        assert report_data.is_element_in_list("") == []

    def test_report_data_find_elements_based_combination(self):
        """Return elements based combination"""
        path = Path(
            "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
        sample_dataset = loads(path.read_text(encoding="utf-8"))
        report_data = ReportData(sample_dataset)

        elements1 = report_data.find_elements_based_combination(
            "102010-VG_201-ML_11-AE_11-*-D")
        elements3 = report_data.find_elements_based_combination(
            "102010-*-*-*-*-D")

        assert elements1 == [
            "Note-FinancialInvestments-Short-Shares-Acquisition"]

        assert elements3 == [
            "BS-AssetsShort-FinancialInvestments",
            "BS-AssetsShort-Total",
            "BS-Assets-Total",
            "Note-ReceivablesAndPrepayments-Total",
            "Note-ReceivablesAndPrepayments-Short-Total"
        ]

    def test_calcucate_elements_values(self):
        """Test report element calculations"""
        path = Path(
            "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
        sample_dataset = loads(path.read_text(encoding="utf-8"))
        report_data = ReportData(sample_dataset)
        report_data.calcucate_elements_values()

        assert len(report_data.report_elements) > 1

    def test_generate_account_combination_report_elements_mapping_rules(self):
        path = Path(
            "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
        sample_ledger = loads(path.read_text(encoding="utf-8"))
        report_data = ReportData(sample_ledger)
        mapping = report_data.generate_account_combination_report_elements_mapping_rules()
        assert len(mapping) > 1

    def test_return_elements(self):
        path = Path(
            "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
        sample_dataset = loads(path.read_text(encoding="utf-8"))
        report_data = ReportData(sample_dataset)
        report_elements_for_xbrl = report_data.return_report_elements()

        assert len(report_elements_for_xbrl) > 1
