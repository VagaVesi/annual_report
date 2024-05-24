"""Make report element pattern

Input: xls file with combinations
Output: json file with pattern
"""

from datetime import datetime
import time
import pandas as pd
import json
INPUT_FILE = "annual_report/tools/input/Elementide_seosed.xlsx"
SHEET_NAME = "final"
OUTPUT_FILE = "annual_report/tools/output/report_element_pattern.json"


class Pattern:
    """Make pattern file from source data"""

    def __init__(self) -> None:
        self.source_data = []
        self.patterns = {"created": "",
                         "Report element pattern": []}

    def load_source_data(self, file_name=INPUT_FILE, sheetname=SHEET_NAME, skip_rows=0) -> None:
        """Make dictionary from xls source
        xls_raw: xls source form load_data_from_excel
        retuns: result in dictionary format
        """
        xls_raw = self.load_data_from_excel(file_name, sheetname, skip_rows)
        result = []
        if xls_raw != None:
            elements_count = len(xls_raw['Element-code'])
            for i in range(0, elements_count):
                element = {}
                for x, y in xls_raw.items():
                    if pd.notna(y[i]):
                        if x == 'Element-code':
                            element['code'] = str(y[i])
                        if x == 'MainAccount':
                            element['MAJANDUSLIKSISU2024ap'] = str(y[i])
                        if x == 'AssetTypeId':
                            if str(y[i]) != None:
                                element['VARAGRUPP2024ap'] = str(y[i])
                        if x == 'PresentationId':
                            if str(y[i]) != None:
                                element['ANDMETEESITLUSVIIS2024ap'] = str(y[i])
                        if x == 'ChangeTypeId':
                            if str(y[i]) != None:
                                element['MUUTUSELIIK2024ap'] = str(y[i])
                        if x == 'RelatedPartyId':
                            if str(y[i]) != None:
                                element['SEOTUDOSAPOOL2024ap'] = str(y[i])
                        if x == 'debitCreditCode':
                            if str(y[i]) != None:
                                element['DEBIT_CREDIT'] = str(y[i])
                result.append(element)
        self.source_data = result

    def load_data_from_excel(self, file_name=INPUT_FILE, sheetname=SHEET_NAME, skip_rows=0) -> dict:
        """Load data from excel file."""
        try:
            loaded_data = pd.read_excel(
                io=file_name, sheet_name=sheetname, skiprows=skip_rows)
            return loaded_data.to_dict()
        except Exception as e:
            print("File not found: " + file_name)
            return None

    def generate_combinations(self, file_name=INPUT_FILE, sheetname=SHEET_NAME, skip_rows=0) -> None:
        """Generates report element patttern"""
        if len(self.source_data) == 0:
            self.load_source_data(file_name, sheetname, skip_rows)
        result = []
        for item in self.source_data:
            element = {}
            for k, v in item.items():
                if k == "code":
                    element["code"] = clear_string(v)
                elif k == "DEBIT_CREDIT":
                    if v != "":
                        element["DEBIT_CREDIT"] = v
                else:
                    combinations = return_pattern_and_elements_from_string(v)
                    if len(combinations[0]) > 0:
                        if "pattern" in element.keys():
                            element["pattern"][k] = combinations[0]
                        else:
                            element["pattern"] = {k: combinations[0]}
                    if len(combinations[1]) > 0:
                        if "elements" in element.keys():
                            element["elements"][k] = combinations[1]
                        else:
                            element["elements"] = {k: combinations[1]}
            result.append(element)
        self.patterns["Report element pattern"] = result
        self.update_timestamp()

    def update_timestamp(self):
        """Update pattern creation date"""
        self.patterns["created"] = datetime.fromtimestamp(
            time.time()).strftime("%Y-%m-%d")

    def save_dict_to_json_file(self, file_name=OUTPUT_FILE) -> bool:
        """Save dict to JSON file"""
        try:
            with open(file_name, "w", encoding='utf-8') as outfile:
                json_object = json.dumps(
                    self.patterns, indent=4, ensure_ascii=False)
                outfile.write(json_object)
                return True
        except:
            print("Saving data failed!")
            return False


def make_pattern(elements: list) -> str:
    """Make regex pattern based list"""
    pattern = ""
    if len(elements) > 1:
        pattern = pattern + "^"
        for x in range(len(elements[0])):
            combinations = set()
            for item in elements:
                combinations.add(item[x])
            combinations = sorted(list(combinations))
            string_list = ""
            for item in combinations:
                string_list = string_list + item
            if len(string_list) == 1:
                pattern = pattern + string_list
            else:
                pattern = pattern + "[" + string_list + "]"
    else:
        pattern = "^" + elements[0]
    if pattern.count("*") > 0:
        for x in range(pattern.count("*"), 0, -1):
            string_count = "\\d{" + str(x) + "}"
            replace_string = x * "*"
            pattern = pattern.replace(replace_string, string_count)
    pattern = pattern + "$"
    return pattern


def return_pattern_and_elements_from_string(string_of_elements: str) -> tuple:
    """Return pattern and elements """
    pattern_elements = []
    pattern = ""
    standard_elements = []
    codes = string_of_elements.split(",")
    for code in codes:
        if "*" in code:
            pattern_elements.append(code.strip())
        else:
            standard_elements.append(code.strip())
    if len(pattern_elements) > 0:
        pattern = make_pattern(pattern_elements)
    return (pattern, standard_elements)


def clear_string(sentence: str) -> str:
    """Correct typos in element name string"""
    return sentence.replace(u"\u00A0", "").strip()
