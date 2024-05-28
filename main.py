"""Call all functions to simulatete annual accounts process."""

# from path import Path
# from json import loads
# from report_data.report_data import ReportData, generate_report_element_filtering_rules, save_as_json
# from tools.json_validator import validate
# from classifications.classification import ClassificationsList
from agregator.agregator import save_ledger, generate_ledger_from_entries
# from classifications.classification import ClassificationsList
# from annual_report.report_data.pattern import Pattern


def main():
    """Run all steps needed for testing."""
    """Load all classifications needed."""
    # cls = ClassificationsList(do_update=True)
    # cls.update_classification_elements()

    """Generate pattern json from xls"""
    # pattern = Pattern()
    # pattern.generate_combinations()
    # pattern.save_to_json_file()

    """Generate report elements from dataset"""
    # mapping1 = generate_report_element_filtering_rules()
    # save_as_json(mapping1, "report_element_accounts_filter_rules")

    """Generate from transactions file a dataset file."""
    # sample_ledger_micro = generate_ledger_from_entries("annual_report/tests/entry/modified_entries_list.json", ["EE0301010"],
    #                                                    "11308014", "2023-01-01", "2023-12-31")
    # save_ledger(sample_ledger_micro)

    sample_ledger_standard = generate_ledger_from_entries("annual_report/tests/entry/modified_entries_list.json", ["EE0301020",  "EE0302010"],
                                                          "13333333", "2023-01-01", "2023-12-31")
    save_ledger(sample_ledger_standard)

    """Validate json file."""
    # file_name = "annual_report/agregator/output/11308014-2024-05-13T14:14:07:726.json"
    # schema = "annual_report/json_shemas/EE0301020_schema.json"

    # if Path(file_name).exists():
    #     dataset = loads(Path(file_name).read_text())
    # result = validate(dataset, schema)
    # print(result)

    """Generate report elements for micro"""
    # path = Path(
    #     "annual_report/tests/report_data/source_data/sample_dataset_micro.json")
    # sample_dataset = loads(path.read_text(encoding="utf-8"))
    # report_data = ReportData(sample_dataset)
    # save_as_json(report_data.account_combinations_mapping,
    #              "account_combination_report_elements_mapping")

    # report_elements_for_xbrl = report_data.return_report_elements()
    # print(report_elements_for_xbrl)


if __name__ == "__main__":
    main()
