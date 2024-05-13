"""Agregator finds available combinations and agregates debit and credit amounts."""
from datetime import datetime
from json import dumps

from path import Path
from entry.entry import load_entries
import time

DATASET_OUTPUT_PATH = "annual_report/agregator/output/"


class AgregatorEntries:
    """Agregate data by column combinations"""

    def __init__(self, file_path: str) -> None:
        """Stores entry details for calculations in normalized structure."""
        self.entries = []
        self.combinations = {}

        for entry in load_entries(file_path)["entries"]:
            for entrydetail in entry["entryDetail"]:
                entry_normalized = {
                    "hash": {},
                    "MainAccountId": entrydetail["accountMain"]["accountMainID"],
                    "PresentationId": "",
                    "AssetTypeId": "",
                    "ChangeTypeId": "",
                    "CountryId": "",
                    "RelatedPartyId": "",
                    "ActivityId": "",
                    "DebitAmount": 0.0,
                    "CreditAmount": 0.0
                }
                if "accountSub" in entrydetail.keys():
                    for key, value in entrydetail["accountSub"].items():
                        if key == "ANDMETEESITLUSVIIS2024ap":
                            entry_normalized["PresentationId"] = value
                        elif key == "VARAGRUPP2024ap":
                            entry_normalized["AssetTypeId"] = value
                        elif key == "MUUTUSELIIK2024ap":
                            entry_normalized["ChangeTypeId"] = value
                        elif key == "RTK2T2013ap":
                            entry_normalized["CountryId"] = value
                        elif key == "SEOTUDOSAPOOL2024ap":
                            entry_normalized["RelatedPartyId"] = value
                        elif key == "EMTAK2008ap":
                            entry_normalized["ActivityId"] = value
                if entrydetail["debitCreditCode"] == "D":
                    entry_normalized["DebitAmount"] = entrydetail["amount"]
                else:
                    entry_normalized["CreditAmount"] = entrydetail["amount"]
                combination = (entry_normalized["MainAccountId"],
                               entry_normalized["PresentationId"],
                               entry_normalized["AssetTypeId"],
                               entry_normalized["ChangeTypeId"],
                               entry_normalized["RelatedPartyId"],
                               entry_normalized["CountryId"],
                               entry_normalized["ActivityId"]
                               )
                entry_normalized["hash"] = hash(combination)
                self.entries.append(entry_normalized)
                self.combinations[entry_normalized["hash"]] = combination

    def aggregate_combination_amounts(self) -> list:
        """Return combination and debit and credit amount total"""
        result = []
        for hash, combination in self.combinations.items():
            debit_amount_sum = 0.0
            credit_amount_sum = 0.0
            filted_rows = list(
                filter(lambda row: (row["hash"] == hash), self.entries))
            for item in filted_rows:
                debit_amount_sum = debit_amount_sum + item["DebitAmount"]
                credit_amount_sum = credit_amount_sum + item["CreditAmount"]
            result.append({"Combination": combination, "Debit_total": debit_amount_sum,
                          "Credit_total": credit_amount_sum})
        return result

    def get_aggregated_entryDetail_for_dataset(self) -> list:
        """Return agregated data as entryDetail."""
        entryDetail = []
        line_number = 1
        for item in self.aggregate_combination_amounts():
            debit_minus_credit = item["Debit_total"] - item["Credit_total"]
            if debit_minus_credit == 0:
                continue
            debit_credit_code = "D" if debit_minus_credit > 0 else "C"
            entry_row = {"lineNumberCounter": line_number, "accountMainID": item["Combination"][0],
                         "debitCreditCode": debit_credit_code, "amount": abs(debit_minus_credit)}
            account_subs = {}
            if item["Combination"][1] != "":
                account_subs["ANDMETEESITLUSVIIS2024ap"] = item["Combination"][1]
            if item["Combination"][2] != "":
                account_subs["VARAGRUPP2024ap"] = item["Combination"][2]
            if item["Combination"][3] != "":
                account_subs["MUUTUSELIIK2024ap"] = item["Combination"][3]
            if item["Combination"][4] != "":
                account_subs["RTK2T2013ap"] = item["Combination"][4]
            if item["Combination"][5] != "":
                account_subs["SEOTUDOSAPOOL2024ap"] = item["Combination"][5]
            if item["Combination"][6] != "":
                account_subs["EMTAK2008ap"] = item["Combination"][6]
            if len(account_subs) > 0:
                entry_row["accountSub"] = account_subs
            entryDetail.append(entry_row)
            line_number += 1
        return entryDetail


def generate_dataset_from_entries(file_path: str, entity_id: str, period_start: str, period_end: str) -> dict:
    """Aggregate data from entries and generate dataset.

    param: 
    file path(str): path to json file with entries  
    entity_id(str): entity identification code
    period_start(str): dataset period start in format 'YYYY-MM-DD'
    period_en(str): dataset period end in format 'YYYY-MM-DD'

    result: dataset
    """
    source_data = AgregatorEntries(file_path)
    agregated_data = source_data.get_aggregated_entryDetail_for_dataset()
    report_timestamp = datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%dT%H:%M:%S:%f")
    return {
        "documentInfo":
        {
            "uniqueID": f"{entity_id}-{report_timestamp[0:-3]}",
            "language": "iso639:et",
            "creationDate": report_timestamp[0:10],
            "creator": "EE37903216506",
            "periodCoveredStart": period_start,
            "periodCoveredEnd": period_end,
            "sourceApplication": "python-test",
            "defaultCurrency": "iso4217:eur"
        },
        "entityInformation": {
            "organizationIdentifier": entity_id,
            "organizationDescription": "e-äriregister"
        },
        "datasets": [
            {
                "entryNumber": "EE0301020",
                "entryDetail": agregated_data
            }
        ]
    }


def save_dataset(dataset_data: dict, dir=DATASET_OUTPUT_PATH):
    """Save dataset data to json file"""
    filename = dataset_data["documentInfo"]["uniqueID"]

    path = Path(dir + filename+".json")
    path.write_text(dumps(dataset_data, indent=4,
                    ensure_ascii=False), encoding="utf-8")
