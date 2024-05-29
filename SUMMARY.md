# Classes

## Agregator

Calculate total amounts based on source data. For group by source data combinations are normalized. Return correct Debit or Credit based total amounts.

1. AgregatorEntries - agregate possible combinations from entries json file
2. AgregatorEntriesDataSet - agregate entries for dataset and make Ledger

## Classifications

Get classsification data: elements lists, element name etc.

1. ClassificationsList - load classsifications from API and save result to JSON
2. Classification - hold classification data and its elements
3. Element - hold element details

## Entry

Post entries to json file. Used to create sample data for test datasets.

1. Entry - hold entry header and entry details
2. EntryDetail - hold entry row details

## ReportData

Make report elements from Ledger

1. Pattern - make mapping pattern json from xls source file
2. ReportData - generate ReporElements based on ledger and pattern
3. ReportElement - hold source data and calculate its value based

## Report

Planned to use to generate XBRL2 test Report from report data
