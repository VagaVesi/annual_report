from annual_report.agregator.agregator import AgregatorEntries, generate_ledger_from_entries


class TestAgregator():
    """Tests for entries agregator class."""

    def test_init_agregator_entries(self):
        ag = AgregatorEntries("annual_report/tests/entry/one_entry.json")
        assert len(ag.entries) > 0

    def test_generate_ledger_from_entries_dataset_changes(self):
        """Test"""
        sample_ledger_standard = generate_ledger_from_entries("annual_report/tests/entry/modified_entries_list.json", ["EE0302010"],
                                                              "13333333", "2023-01-01", "2023-12-31")
        assert sample_ledger_standard["datasets"][0]["entryNumber"] == "EE0302010"
