"""Call all functions to simulatete annual accounts process."""
from path import Path
from classifications.classification import ClassificationsList, CLASSIFICATION_ELEMENTS_SCHEMA, CLASSIFICATIONS_LIST_SCHEMA
from tools.validator import validate_json
from tools.api_request import request_data
from json import loads


def main():
    """Run all steps needed for testing."""
    # Load all classifications needed

    cls = ClassificationsList(do_update=True)
    cls.update_classification_elements()

    # response = request_data(
    #     "https://demo-datahub.rik.ee/api/v1/meta/classifications/MAJANDUSLIKSISU2024ap")
    # print(response)

    # data = loads(Path(
    #     "annual_report/classifications/download/test.json").read_text())
    # validation_result = validate_json(
    #     data, "annual_report/json_shemas/classification_elements_schema.json")
    # print(validation_result)


if __name__ == "__main__":
    main()
