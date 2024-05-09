"""Module to store XBRL-GL classifications."""
from path import Path
from json import dumps, loads
from tools.api_request import get_data
from annual_report.tools.json_validator import validate


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

    def get_links(self) -> dict:
        """Returns classifivcation code - get link pairs."""
        links = {}
        for item in self.classifications:
            links[item["code"]] = item["links"]["get"]
        return links

    def update_classification_elements(self):
        """Load all classification elements and save to file"""
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


class Classification:
    """Class for XBRL-GL classification."""

    def __init__(self, classification_code: str) -> None:
        pass

    def is_code_valid(code: str) -> bool:
        """Check is classification code valid.

        params: 
        code (str): Code to validate

        returns (boolean): If valid return True   
        """
        pass
