# Annual Report Test Project

Steps

1. Load classifications from API, validate input - OK
2. Prepare Classification and its element object - OK
3. Prepare sample XBRL GL entry file in JSON format, add Entries to JSON file - OK
4. Generate one dataset from sample XBRL GL transactions. Save file - OK
5. Validate one dataset with schema - OK
6. Prepare report mapping rules (JSON format) - OK
7. Convert XBRL-GL annual one dataset to Annual Report elements using mapping rules -> store result in json - OK
8. Prepare mapping rules json from xls - OK
9. Add Debit and Credit for element selection logic - OK
10. Add validation checks for Annual Report elements
    - Missing combinations in mapping
    - Some basic element comparsions
11. Generate simple Annual Report object from Annual Report elements

# ADDITIONAL FEATURES:

1. Modify source dataset based on dataset code (balances and movements) - OK
2. Save several datasets to one file - OK
3. Make report elements from multiple datasets - OK
4. Related parties additional info (separate set of data) - have to eliminate from standard dataset (except investments)
5. Countries and activityType additional info

# LIVE TO ADD

1. Pattern input validation (Complex pattern OR is not supported in prototype)
2. Ledger agregator: replace datsets_list -> report_code
