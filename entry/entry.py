"""Validate sample entries."""
from datetime import date
from json import dumps, loads

from path import Path
from annual_report.classifications.classification import CLASSIFICATION_DOWNLOAD_PATH
from entry.entry_validation_error import EntryValidationError, ValidationErrorType

SAMPLE_ENTRIES_FILE = "annual_report/sample_data/sample_entries.json"


class Entry:
    """Holds entry data."""

    def __init__(self, entry_number: str, posting_date: date, decription: dict, entry_details: list) -> None:
        """Init Entry.

        params:
        entry_ref (str): reference to source document
        posting_date (date): entry rosting date
        decription (dict): entry description language string pairs 
        entry_details (EntryDetail): List of entry lines
        """
        self.entry_ref = entry_number
        self.date = posting_date
        self.decription = decription
        self.entry_details = entry_details


class EntryDetail:
    """Holds entry row data."""

    def __init__(self, line_number: int, account_main_id: str, account_sub_list: dict, debit_credit: str, amount: float) -> None:
        """Entry row.

        params:
        line_number (int): Entry row number
        account_main_id (str): MainAccount id 
        account_sub_list (dict): Subaccount classification and element pairs.
        debit_credit (str) : Debit = D, Credit = C
        amount(float): row amount in local currency 
        """
        self.line_number = line_number
        self.main_account = account_main_id
        self.sub_account = account_sub_list
        self.debit_credit = debit_credit
        self.amount = amount


def validate_entry(entry: Entry) -> list:
    """Run all entry validations. Return empty list if no errors."""

    errors = []

    if abs(calculate_entry_debit_total_minus_credit_total(entry)) > EntryValidationError.NOT_MATERIAL_DIFFERENCE:
        errors.append(EntryValidationError(
            ValidationErrorType.DEBIT_NOT_EQUALS_CREDIT, entry.entry_ref))

    return errors


def calculate_entry_debit_total_minus_credit_total(entry: Entry) -> float:
    """Calculate entry debit and credit amouts difference."""

    debit_total = 0.00
    credit_total = 0.00

    for row in entry.entry_details:
        if row.debit_credit == "D":
            debit_total = debit_total + row.amount
        else:
            credit_total = credit_total + row.amount

    return round(debit_total-credit_total, 2)


def add_simple_entry_to_json_file(
        posting_date: date,
        decription: dict,
        amount: float,
        debit_main_account: str,
        credit_main_account: str,
        debit_sub_account={},
        credit_sub_account={},
        file_path=SAMPLE_ENTRIES_FILE):
    """Add simple entry (one debit, on credit) to entries file."""

    sample_entries = load_entries(file_path)
    new_entry = Entry(get_next_entry_number(sample_entries), posting_date, decription, [EntryDetail(
        1, debit_main_account, debit_sub_account, "D", amount), EntryDetail(2, credit_main_account, credit_sub_account, "C", amount)])
    sample_entries["entries"].append(make_dict_from_entry(new_entry))
    save_entries(file_path, sample_entries)


def load_entries(file_path: str) -> dict:
    """Load sample entries to dict."""

    sample_entries = {
        "entity": "empty_entity",
        "entries": []
    }
    path = Path(file_path)
    if path.exists():
        sample_entries = loads(path.read_text(encoding="utf-8"))
    return sample_entries


def save_entries(file_path: str, entries: dict):
    """Save sample entries from list fo json file."""

    path = Path(file_path)
    path.write_text(
        dumps(entries, indent=4, ensure_ascii=False), encoding="utf-8")


def get_next_entry_number(entity_entries: dict) -> int:
    """Return next entry number"""

    if len(entity_entries["entries"]) > 0:
        entry_numbers = []
        for entry in entity_entries["entries"]:
            entry_numbers.append(entry["entryHeader"]["entryNumber"])
        return max(entry_numbers) + 1
    else:
        return 1


def make_dict_from_entry(entry: Entry) -> dict:
    """Make custom dictionary fron Entry object."""

    response = {"entryHeader": {"entryNumber": entry.entry_ref,
                                "postingDate": entry.date,
                                "decription": {
                                    "en": entry.decription
                                }},
                "entryDetail": []}

    for item in entry.entry_details:
        line = {
            "lineNumber": item.line_number,
            "accountMain": {
                "accountMainID": item.main_account,

            },
            "debitCreditCode": item.debit_credit,
            "amount": item.amount
        }
        response["entryDetail"].append(line)

        if len(item.sub_account) > 0:
            line["accountSub"] = item.sub_account

        line["accountMain"]["name"] = get_main_account_name(
            item.main_account)

    return response


def get_main_account_name(main_account_id: str, languages=["et"]) -> dict:
    """Return MainAccount name basded on language codes."""
    name = {}
    path = Path(CLASSIFICATION_DOWNLOAD_PATH + "MAJANDUSLIKSISU2024ap.json")
    if path.exists():
        classification = loads(path.read_text(encoding="utf-8"))
        for element in classification["elements"]:
            if element["code"] == main_account_id:
                for lang in languages:
                    name[lang] = element["name"][lang]
    return name
