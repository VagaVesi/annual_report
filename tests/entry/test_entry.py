"""Test Entry class and functions."""
from datetime import date
from annual_report.entry.entry import Entry, EntryDetail, calculate_entry_debit_total_minus_credit_total, load_entries, get_next_entry_number, add_simple_entry_to_json_file, make_dict_from_entry, make_entry_from_json, make_entry_list_from_json_list


class TestEntry():
    """Tests for Entry class."""

    def test_init_simple_entry_detail(self):
        """Init simple EntryDetail"""
        entry_line_1 = EntryDetail(1, "101010", [], "D", 2500.00)

        assert entry_line_1.amount == 2500.00
        assert entry_line_1.debit_credit == "D"
        assert entry_line_1.line_number == 1
        assert entry_line_1.sub_accounts == []

    def test_calculate_entry_debit_total_minus_credit_total_equal_no_diffrenece(self):
        """Debit and Credit equal, difference 0.0"""
        sample_entry = Entry("fin.1", "2020-01-01", "Cash to bank", [EntryDetail(
            1, "101010", {}, "D", 1003.01), EntryDetail(2, "101040", {}, "C", 103.01), EntryDetail(3, "101030", {}, "C", 900.00)])

        assert calculate_entry_debit_total_minus_credit_total(
            sample_entry) == 0.00

    def test_calculate_entry_debit_total_minus_credit_total_debit_bigger(self):
        """Debit is bigger, difference positive amount."""
        sample_entry = Entry("fin.1", "2020-01-01", "Cash to bank", [EntryDetail(
            1, "101010", {}, "D", 1006.02), EntryDetail(2, "101040", {}, "C", 103.01), EntryDetail(3, "101030", {}, "C", 900.00)])

        assert calculate_entry_debit_total_minus_credit_total(
            sample_entry) == 3.01

    def test_calculate_entry_debit_total_minus_credit_total_credit_bigger(self):
        """Credi is bigger, difference negative amount."""
        sample_entry = Entry("fin.1", "2020-01-01", "Cash to bank", [EntryDetail(
            1, "101010", {}, "D", 1000.02), EntryDetail(2, "101040", {}, "C", 103.01), EntryDetail(3, "101030", {}, "C", 900.00)])

        assert calculate_entry_debit_total_minus_credit_total(
            sample_entry) == -2.99

    def test_load_sample_entries(self):
        """File opened and data loaded."""
        sample_data = load_entries(
            "annual_report/tests/entry/one_entry.json")

        assert len(sample_data["entries"]) > 0
        assert sample_data["entity"] == "small_company"

    def test_get_next_entry_number_one_entry(self):
        """If first_entry_list next entry number is 1."""
        sample_data = load_entries(
            "annual_report/tests/entry/one_entry.json")

        assert get_next_entry_number(sample_data) == 2

    def test_get_next_entry_number_empty_entrylist(self):
        """list next entry number is current + 1."""
        sample_data = load_entries(
            "annual_report/tests/entry/empty_entry_list.json")

        assert get_next_entry_number(sample_data) == 1

    def test_make_dict_from_simple_entry(self):
        """Make dict from simple_entry_to save entry json file.

        Simple entry -> One debit and credit no subaccounts.
        """
        sample_entry = Entry("fin.1", "2020-01-01", "Cash to bank", [EntryDetail(
            1, "101010", {}, "D", 1003.01), EntryDetail(2, "101020", {}, "C", 103.01), EntryDetail(3, "101030", {}, "C", 900.00)])

        expected_result = {
            "entryHeader": {
                "entryNumber": "fin.1",
                "postingDate": "2020-01-01",
                "decription": {"en": "Cash to bank"}
            },
            "entryDetail": [
                {
                    "lineNumber": 1,
                    "accountMainID": "101010",
                    "debitCreditCode": "D",
                    "amount": 1003.01
                },
                {
                    "lineNumber": 2,
                    "accountMainID": "101020",
                    "debitCreditCode": "C",
                    "amount": 103.01
                },
                {
                    "lineNumber": 3,
                    "accountMainID": "101030",
                    "debitCreditCode": "C",
                    "amount": 900.00
                }
            ]
        }

        calculated_result = make_dict_from_entry(sample_entry)
        assert calculated_result == expected_result

    def test_add_simple_entry_to_json_file(self):
        """Load original_list, add entry to list and save modified_list to file. No Subaccounts"""
        sample_data = load_entries(
            "annual_report/tests/entry/modified_entries_list.json")
        entries_count_before = len(sample_data["entries"])
        add_simple_entry_to_json_file(str(date.today()), "Test simple entry", 200.00, "101020",
                                      "418012", {}, {"EMTAK2008ap": "07101"}, file_path="annual_report/tests/entry/modified_entries_list.json")
        sample_data = load_entries(
            "annual_report/tests/entry/modified_entries_list.json")
        entries_count_after = len(sample_data["entries"])

        assert entries_count_after == entries_count_before + 1

    def test_make_entry_from_json(self):
        sample_entry_json = {
            "entryHeader": {
                "entryNumber": 1,
                "postingDate": "2023-01-15",
                "decription": {"et": "Sissemakse osakapitali", "en": "Contribution to share capital"}
            },
            "entryDetail": [
                {
                    "lineNumber": 1,
                    "accountMainID": "101020",
                    "debitCreditCode": "D",
                    "amount": 2500.00
                },
                {
                    "lineNumber": 2,
                    "accountMainID": "315011",
                    "accountSub": {"MUUTUSELIIK2024ap": "ML_11"},
                    "debitCreditCode": "C",
                    "amount": 2500.00
                }
            ]
        }

        entry = make_entry_from_json(sample_entry_json)
        assert entry.entry_number == 1
        assert entry.entry_details[0].main_account == "101020"
        assert entry.entry_details[1].main_account == "315011"
        assert entry.entry_details[0].sub_accounts == {}
        assert entry.entry_details[1].sub_accounts == {
            "MUUTUSELIIK2024ap": "ML_11"}

    def test_make_entry_list_from_json_list(self):
        sample_json = load_entries(
            "annual_report/tests/entry/modified_entries_list.json")
        input_length = len(sample_json["entries"])
        entries_list = make_entry_list_from_json_list(sample_json)

        assert len(entries_list) == input_length
