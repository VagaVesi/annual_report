"""Module to store XBRL-GL classifications."""
from path import Path
from json import dumps, loads
from tools.api_request import get_data
from datetime import date
from tools.json_validator import validate


CLASSIFICATION_DOWNLOAD_PATH = "annual_report/classifications/download/"
CLASSIFICATIONS_API_PATH = "https://demo-datahub.rik.ee/api/v1/meta/classifications"
CLASSIFICATIONS_LIST_SCHEMA = "annual_report/json_shemas/classifications_list_schema.json"
CLASSIFICATION_ELEMENTS_SCHEMA = "annual_report/json_shemas/classification_elements_schema.json"


class ClassificationsList:
    """Class for Classifications list."""

    def __init__(self, do_update=False) -> None:
        """Init ClassificationsList.

        param:
        update (boolean): update classification list from API if True
        """
        self.classifications = self.load_classifications_list(do_update=False)

    def load_classifications_list(self, do_update=False) -> list:
        """load classications list from directory or from API.

        Default is from local file, if file exists. To update local file
        content set do_update=True

        params:
        update (boolean): update classification list from API if True
        returns: List on classifications in JSON format
        """
        classifications = []

        path = Path(CLASSIFICATION_DOWNLOAD_PATH + "classifications.json")
        if path.exists():
            classifications = loads(path.read_text(encoding="utf-8"))
        else:
            do_update = True

        if do_update:
            classifications_update = get_data(CLASSIFICATIONS_API_PATH)
            validation_result = validate(
                classifications_update, CLASSIFICATIONS_LIST_SCHEMA)
            if len(validation_result) > 0:
                print(validation_result)
            else:
                path.write_text(dumps(classifications_update,
                                indent=4, ensure_ascii=False), encoding="utf-8")
                classifications = classifications_update
        return classifications

    def update_classification_elements(self):
        """Download classifications elementss from API and save to file."""
        for code, api_link in self.get_links().items():
            file_path = CLASSIFICATION_DOWNLOAD_PATH + code + ".json"
            path = Path(file_path)
            classifications_update = get_data(api_link)
            validation_result = validate(
                classifications_update, CLASSIFICATION_ELEMENTS_SCHEMA)
            if len(validation_result) > 0:
                print(validation_result)
            else:
                path.write_text(dumps(classifications_update,
                                indent=4, ensure_ascii=False), encoding="utf-8")

    def get_links(self) -> dict:
        """Returns links to download classifications.

        result: pairs: classification code - link."""
        links = {}
        for item in self.classifications:
            links[item["code"]] = item["links"]["get"]
        return links


class Classification:
    """Class for XBRL-GL classification."""

    def __init__(self, classification_code: str) -> None:
        """Init classification object from JSON file."""
        path = Path(CLASSIFICATION_DOWNLOAD_PATH +
                    classification_code + ".json")

        if path.exists():
            classification = loads(path.read_text(encoding="utf-8"))
            self.code = classification["code"]
            self.name = classification["name"]
            self.__elements = make_elements_list(classification["elements"])
            self.element_codes = set()
            if len(self.element_codes) == 0:
                for item in self.__elements:
                    self.element_codes.add(item.code)

    @property
    def elements(self):
        return self.__elements

    def is_code_correct(self, element_code: str) -> bool:
        """Check if classification code exists.

        initialises classification elements_codes set 

        params:
        code (str): Element code to validate

        returns (boolean): If valid return True
        """

        if element_code in self.element_codes:
            return True
        else:
            return False

    def get_element_name(self, element_id: str, languages=["et"]) -> dict:
        """Return MainAccount name basded on language codes."""
        if self.is_code_correct(element_id):
            for element in self.elements:
                if element.code == element_id:
                    return element.get_name(languages)


class Element:
    """Class for classification element"""

    def __init__(self, code: str, name: dict, valid_from_date: str, valid_until_date=None) -> None:
        """Init classification element"""
        self.code = code
        self.name = name
        self.valid_from_date = date.fromisoformat(valid_from_date)
        self.valid_until_date = None if valid_until_date == None else date.fromisoformat(
            valid_until_date)

    def get_name(self, languages=["et"]) -> dict:
        """Return Element name based on language codes."""
        name = {}
        for lang in languages:
            name[lang] = self.name[lang]
        return name

    def was_valid(self, period_start: date, period_end: date) -> bool:
        """Return was element valid between dates"""
        if period_end < period_start:
            return False
        # TODO
        pass


def make_elements_list(elements: list) -> list:
    """Create Elements objects list from list of dict."""
    result = []
    for element in elements:
        if "valid_until_date" in element.keys():
            valid_until = element["valid_until_date"]
        else:
            valid_until = None
        result.append(Element(element["code"], element["name"],
                      element["valid_from_date"], valid_until))
    return result
