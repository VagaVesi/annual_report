"""Validate report data using validation mapping.

Validation rules are selected based on target element.
Target element hierarhy:
- Main reports (BS & IS) rules
- Note Total amount -> Main report amount
- Note Total amount -> Note items amounts total
- Note other total comparsions (x and y axis) (N/A in datahub)
- Main report CF -> to several other parts of report (N/A in datahub)
"""


from json import loads
from path import Path

REPORT_ELEMENTS_VALIDATION_RULES_PATH = "annual_report/report_data/source_data/report_elements_validation_mapping_sample.json"


class ReportDataValidator():
    """Validate ReportData output"""

    def __init__(self, report_elements: list) -> None:

        self.report_elements = report_elements
        self.validation_rules = load_validation_rules()
        self.validation_result = []

    def validate(self) -> list:
        """Validates report elements and return errors list."""
        if len(self.report_elements) > 1:
            for element in self.report_elements:
                self.validation_result = self.validation_result + \
                    self.add_target_element_validation_rules(element["code"])
        if len(self.validation_result) > 1:
            for item in self.validation_result:
                item["amounts-comparsion-result"] = self.compare_total_amounts(
                    item)
        return self.filter_errors()

    def filter_errors(self) -> list:
        """Returns validation result errors"""
        return list(filter(lambda x: (x["amounts-comparsion-result"] != 0), self.validation_result))

    def add_target_element_validation_rules(self, element_code: str) -> list:
        """Find element validation rules based on element code."""
        result = []
        for item in self.validation_rules:
            if item["target-element"] == element_code:
                result.append(item)
        return result

    def compare_total_amounts(self, validation_rule: dict) -> float:
        """Find elements comparsion difference."""
        target_value = self.find_total_amount(
            [validation_rule["target-element"]])
        compare_value = self.find_total_amount(
            validation_rule["compare-to-elements"])
        return target_value - compare_value

    def find_total_amount(self, element_codes: list) -> float:
        """Find report elements total amount."""
        total_amount = 0.00
        for element_code in element_codes:
            filterer_list = list(
                filter(lambda x: (x["code"] == element_code), self.report_elements))
            for element in filterer_list:
                if element["debitCreditCode"] == "D":
                    total_amount = total_amount + element["amount"]
                else:
                    total_amount = total_amount - element["amount"]
        return abs(total_amount)


def load_validation_rules(file_path=REPORT_ELEMENTS_VALIDATION_RULES_PATH) -> list:
    """Load validation rules."""
    result = {}
    path = Path(file_path)
    if path.exists():
        result = loads(path.read_text(encoding="utf-8"))
    return result["Comparing the values of the report elements"]
