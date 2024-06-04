"""Convert dataset data to Annual Report elements."""
from json import dumps, loads
import re
from path import Path

from classifications.classification import Classification
from agregator.agregator import get_normalised_entry_detail

OUTPUT_PATH = "annual_report/report_data/output/"
PATTERN_FILE = "annual_report/report_data/output/report_element_pattern.json"

CLASSIFICATIONS_FOR_PATTERN = ["MAJANDUSLIKSISU2024ap", "SEOTUDOSAPOOL2024ap"]
ELEMENT_CODES = {}


class ReportData():
    """ReportData holds its source data (ledger) and result (report elements)"""

    def __init__(self, ledger: dict, pattern_file=PATTERN_FILE) -> None:
        """Init data to generate report elements."""
        self.source_data = ledger
        self.uniqueID = ledger["documentInfo"]["uniqueID"]
        self.creator = ledger["documentInfo"]["creator"]
        self.sourceApplication = ledger["documentInfo"]["sourceApplication"]
        self.organizationIdentifier = ledger["entityInformation"]["organizationIdentifier"]
        self.periodCoveredStart = ledger["documentInfo"]["periodCoveredStart"]
        self.periodCoveredEnd = ledger["documentInfo"]["periodCoveredEnd"]
        self.datasets = []  # datasets codes are needed for determine report type
        self.report_elements = []
        self.is_values_calculated = False
        self.element_finding_rules = generate_report_element_filtering_rules(
            pattern_file)  # report element : filter input
        self.account_combinations_mapping = self.generate_account_combination_report_elements_mapping_rules(
            pattern_file)  # combination: [report elements]

    def prepare_elements_list(self, dataset: dict):
        """Based on dataset entries prepare report elements."""
        self.datasets.append(dataset["entryNumber"])
        for entrydetail in dataset["entryDetail"]:
            # find combination
            combinations = [entrydetail["accountMainID"]]
            if "accountSub" in entrydetail.keys():
                if "VARAGRUPP2024ap" in entrydetail["accountSub"].keys():
                    combinations = make_combinations(
                        combinations, [entrydetail["accountSub"]["VARAGRUPP2024ap"]])
                else:
                    combinations = make_combinations(combinations, ["*"])
                if "MUUTUSELIIK2024ap" in entrydetail["accountSub"].keys():
                    combinations = make_combinations(
                        combinations, [entrydetail["accountSub"]["MUUTUSELIIK2024ap"]])
                else:
                    combinations = make_combinations(combinations, ["*"])
                if "ANDMETEESITLUSVIIS2024ap" in entrydetail["accountSub"].keys():
                    combinations = make_combinations(
                        combinations, [entrydetail["accountSub"]["ANDMETEESITLUSVIIS2024ap"]])
                else:
                    combinations = make_combinations(combinations, ["*"])
                if "SEOTUDOSAPOOL2024ap" in entrydetail["accountSub"].keys():
                    combinations = make_combinations(
                        combinations, [entrydetail["accountSub"]["SEOTUDOSAPOOL2024ap"]])
                else:
                    combinations = make_combinations(combinations, ["*"])
            else:
                combinations = make_combinations(combinations, ["*-*-*-*"])
            if "debitCreditCode" in entrydetail.keys():
                combinations = make_combinations(
                    combinations, [entrydetail["debitCreditCode"]])
            # add element to report_elements based on combination
            for combination in combinations:
                for element_code in self.find_elements_based_combination(combination):
                    self.add_element_with_entry(element_code, entrydetail)

    def find_elements_based_combination(self, combination: str) -> list:
        """Find elememnts based combination."""
        if combination in self.account_combinations_mapping.keys():
            return self.account_combinations_mapping[combination]
        else:
            return []

    def add_element_with_entry(self, element_name: str, entry: dict):
        """Create ReportElement if not already in list. Add entry data for calculations."""
        is_element = self.is_element_in_list(element_name)
        if len(is_element) == 0:
            element = ReportElement(element_name)
            self.report_elements.append(element)
        else:
            element = is_element[0]
        element.source_data.append(get_normalised_entry_detail(entry))

    def is_element_in_list(self, element_code: str) -> list:
        """Return elements if ReportElement exists in list."""
        filtered = [
            item for item in self.report_elements if item.code == element_code]
        return [] if len(filtered) == 0 else filtered

    def calcucate_elements_values(self):
        """Iter all entries and calculates report elements values."""
        if len(self.report_elements) == 0:
            for dataset in self.source_data["datasets"]:
                self.prepare_elements_list(dataset)
        for element in self.report_elements:
            element.calculate_element_amount()
        self.is_values_calculated = True

    def return_report_elements(self) -> list:
        """Returns calculated report elements list"""
        report_elements = []
        if self.is_values_calculated == False:
            self.calcucate_elements_values()
        for element in self.report_elements:
            report_elements.append(
                {"code": element.code, "debitCreditCode": element.debitCreditCode, "amount": element.amount})
        # TODO add header
        return report_elements

    def generate_account_combination_report_elements_mapping_rules(self, pattern_file=PATTERN_FILE) -> dict:
        """Generate account combination and list of report elements.

        result: dict {mainAccountId-AssetsGroupId-ChangeTypeId-PresentationId-RelatedPartyId-debitCredit: [report element codes]}
        """
        source = self.element_finding_rules if len(
            self.element_finding_rules) > 1 else generate_report_element_filtering_rules(pattern_file)
        result = {}
        for item in source["Report element mapping rules"]:
            combinations = []
            for mainAccountId in item["filter_rule"]["MAJANDUSLIKSISU2024ap"]:
                combinations.append(mainAccountId)
            if "VARAGRUPP2024ap" in item["filter_rule"].keys():
                combinations = make_combinations(
                    combinations, item["filter_rule"]["VARAGRUPP2024ap"])
            else:
                combinations = make_combinations(combinations, ["*"])
            if "MUUTUSELIIK2024ap" in item["filter_rule"].keys():
                combinations = make_combinations(
                    combinations, item["filter_rule"]["MUUTUSELIIK2024ap"])
            else:
                combinations = make_combinations(combinations, ["*"])
            if "ANDMETEESITLUSVIIS2024ap" in item["filter_rule"].keys():
                combinations = make_combinations(
                    combinations, item["filter_rule"]["ANDMETEESITLUSVIIS2024ap"])
            else:
                combinations = make_combinations(combinations, ["*"])
            if "SEOTUDOSAPOOL2024ap" in item["filter_rule"].keys():
                combinations = make_combinations(
                    combinations, item["filter_rule"]["SEOTUDOSAPOOL2024ap"])
            else:
                combinations = make_combinations(combinations, ["*"])
            if "DEBIT-CREDIT" in item["filter_rule"].keys():
                combinations = make_combinations(
                    combinations, item["filter_rule"]["DEBIT-CREDIT"])
            else:
                combinations = make_combinations(combinations, ["*"])
            for combination in combinations:
                if combination not in result.keys():
                    result[combination] = []
                result[combination].append(item["code"])

        # add elements to profit calculations
        bs_items = ["BS-Equity-AnnualPeriodProfitLoss", "BS-Equity-Total",
                    "BS-LiabilitiesAndEquity-Total", "IS-Net-ProfitLoss"]
        for combination, report_elements in result.items():
            if combination[0] in ["4", "5", "6"]:
                for additional_item in bs_items:
                    if additional_item not in report_elements:
                        result[combination].append(additional_item)
            if combination[0:2] in ["520", "521", "522", "619", "623"]:
                if "IS-Operating-ProfitLoss" not in report_elements:
                    result[combination].append("IS-Operating-ProfitLoss")
            if combination[0:2] in ["520", "521", "522", "619", "623", "624"]:
                if "IS-BeforeTax-ProfitLoss" not in report_elements:
                    result[combination].append("IS-BeforeTax-ProfitLoss")
        return result


class ReportElement():
    """Elements holds its calculation data"""

    def __init__(self, code: str) -> None:
        self.code = code
        self.amount = 0.0
        self.debitCreditCode = ""
        self.source_data = []  # entries in normalized format

    def calculate_element_amount(self):
        """Calculates element amount based on entryDetails."""
        debit_amount_sum = 0.0
        credit_amount_sum = 0.0
        for item in self.source_data:
            debit_amount_sum = debit_amount_sum + item["DebitAmount"]
            credit_amount_sum = credit_amount_sum + item["CreditAmount"]
        debit_minus_credit = debit_amount_sum - credit_amount_sum
        if debit_minus_credit != 0:
            self.debitCreditCode = "D" if debit_minus_credit > 0 else "C"
            self.amount = abs(debit_minus_credit)


def load_gl_element_codes():
    """Load classifications element codes."""
    for classification in CLASSIFICATIONS_FOR_PATTERN:
        ELEMENT_CODES[classification] = Classification(
            classification).element_codes


def find_gl_element_codes_based_pattern(classification: str, pattern: str) -> list:
    """Return elements list based on pattern."""
    if len(ELEMENT_CODES) == 0:
        load_gl_element_codes()
    result = []
    for item in ELEMENT_CODES[classification]:
        if re.search(pattern, item) != None:
            result.append(item)
    return result


def generate_report_element_filtering_rules(pattern_file=PATTERN_FILE) -> dict:
    """Generate report element with list of gl-element to select."""
    source_path = Path(pattern_file)
    if source_path.exists:
        mapping_rules = []
        pattern_source = loads(source_path.read_text(encoding="utf-8"))
        for item in pattern_source["Report element pattern"]:
            element_codes = {}
            if "pattern" in item.keys():
                for classification in item["pattern"].keys():
                    element_codes[classification] = find_gl_element_codes_based_pattern(
                        classification, item["pattern"][classification])
            if "elements" in item.keys():
                for classification in item["elements"].keys():
                    if classification in element_codes.keys():
                        element_codes[classification] = element_codes[classification] + \
                            item["elements"][classification]
                    else:
                        element_codes[classification] = item["elements"][classification]
            element_codes["DEBIT-CREDIT"] = item["debit-credit"]
            mapping_rules.append({
                "code": item["code"],
                "filter_rule": element_codes
            })
        return {"Report element mapping rules": mapping_rules}


def make_combinations(list1: list, list2: list) -> list:
    """Make list on combinations based on two list elements"""
    combinations = []
    for i1 in list1:
        for i2 in list2:
            combinations.append(f"{i1}-{i2}")
    return combinations


def save_as_json(data: dict,  output_file_name: str):
    output_path = Path(OUTPUT_PATH + output_file_name + ".json")
    output_path.write_text(
        dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
