"""Convert dataset data to Annual Report elements."""
from json import dumps, loads
import re
from path import Path

from classifications.classification import Classification

CLASSIFICATIONS = ["MAJANDUSLIKSISU2024ap"]
ELEMENT_CODES = {}
SOURCE_DATA_PATH = "annual_report/report_data/source_data/"


class ReportData():
    """Report holds its components"""

    def __init__(self, dataset: dict) -> None:
        """Init data for report based on dataset."""
        self.source_data = dataset
        self.uniqueID = dataset["entityInformation"]["uniqueID"]
        self.creator = dataset["entityInformation"]["creator"]
        self.sourceApplication = dataset["entityInformation"]["sourceApplication"]
        self.organizationIdentifier = dataset["entityInformation"]["organizationIdentifier"]
        self.periodCoveredStart = dataset["documentInfo"]["periodCoveredStart"]
        self.periodCoveredEnd = dataset["documentInfo"]["periodCoveredEnd"]
        self.datasets = []  # datasets codes are for finding report type
        self.report_elements = []
        self.values_calculated = False

    def calcucate_elements_values(self):
        """Iter all elements in list and calculate values."""
        # TODO
        self.values_calculated = True

    def return_result(self) -> dict:
        """Returns calculated elements list as dict"""
        if self.values_calculated == False:
            self.calcucate_elements_values()
        # TODO
        return {}


class ReportElement():
    """Elements holds its calculation data"""

    def __init__(self, code: str) -> None:
        self.code = code
        self.amount = 0.0
        self.debitCreditCode = ""
        self.source_data = []

    def calculate_element_amount(self):
        """Calculates element amount based on entryDetails."""
        # TODO - calculate total amount and find D OR C
        pass


def load_element_codes_lists():
    """Load classifications elements"""
    for classification in CLASSIFICATIONS:
        ELEMENT_CODES[classification] = Classification(
            classification).element_codes


def find_elements_based_pattern(classification: str, pattern: str) -> list:
    """Rerurn list of elements matching pattern"""
    if len(ELEMENT_CODES) == 0:
        load_element_codes_lists()
    result = []
    for item in ELEMENT_CODES[classification]:
        if re.search(pattern, item) != None:
            result.append(item)
    return result


def generate_mapping_rules(pattern_file="report_element_pattern.json", output_file_name="report_element_mapping_rules.json", ):
    """Generate mapping JSON file based on pattern."""
    source_path = Path(SOURCE_DATA_PATH + pattern_file)
    output_path = Path(SOURCE_DATA_PATH + output_file_name)
    if source_path.exists:
        mapping_rules = []
        pattern_source = loads(source_path.read_text(encoding="utf-8"))
        for item in pattern_source["Report element pattern"]:
            element_codes = {}
            if "pattern" in item.keys():
                for classification in item["pattern"].keys():
                    element_codes[classification] = find_elements_based_pattern(
                        classification, item["pattern"][classification])
            if "elements" in item.keys():
                for classification in item["elements"].keys():
                    if classification in element_codes.keys():
                        element_codes[classification] = element_codes[classification] + \
                            item["elements"][classification]
                    else:
                        element_codes[classification] = item["elements"][classification]
            mapping_rules.append({
                "code": item["code"],
                "mapping_rule": element_codes
            })
        rules_update = {"Report element mapping rules": mapping_rules}
        output_path.write_text(dumps(rules_update,
                                     indent=4, ensure_ascii=False), encoding="utf-8")
